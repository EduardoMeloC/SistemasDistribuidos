# region imports, classes and aliases

from __future__ import annotations
import json
from rpyc.utils.server import ThreadedServer
from rpyc.utils.helpers import classpartial

PORT = 18812

# Se não funcionar no lab rode:
# $ pip install --user typing_extensions
import sys

IS_NEW_PYTHON: bool = sys.version_info >= (3, 10)
if IS_NEW_PYTHON:
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from typing import Callable, TYPE_CHECKING, List, Dict, Union, Any
from dataclasses import dataclass

import rpyc  # type: ignore

UserId: TypeAlias = str

Topic: TypeAlias = str

# Isso é para ser tipo uma struct
# Frozen diz que os campos são read-only
if IS_NEW_PYTHON:

    @dataclass(frozen=True, kw_only=True, slots=True)
    class Content:
        author: UserId
        topic: Topic
        data: str

elif not TYPE_CHECKING:

    @dataclass(frozen=True)
    class Content:
        author: UserId
        topic: Topic
        data: str


if IS_NEW_PYTHON:
    FnNotify: TypeAlias = Callable[[list[Content]], None]
elif not TYPE_CHECKING:
    FnNotify: TypeAlias = Callable

# endregion

##############################################
#                                            #
#            BrokerService Schema            #
#                                            #
##############################################
#
# topics: { Topic: [UserId] }
# users: { UserId: UserInfo }
# connections: { conn: UserId }


class UserInfo:
    def __init__(self, online: bool, callback: FnNotify, messages_queue: List[Content]):
        self.online = online
        self.callback = callback
        self.messages_queue = messages_queue


class BrokerData:
    def __init__(self):
        """
        Inicia as Estruturas do Broker: topics, users e userinfo.
        """
        self.__topicsFile = "topics.json"
        self.users: dict[UserId, UserInfo] = {}
        self.topics: dict[Topic, List[UserId]] = {}
        self.connections: dict[Any, UserId] = {}
        self.load_topics_from_file()

    def load_topics_from_file(self):
        """
        Carrega os tópicos a partir de um arquivo de configuração, invocando create_topic
        para cada tópico do arquivo de entrada.
        """
        try:
            with open(self.__topicsFile, "r") as topicsFile:
                topics = json.load(topicsFile)
                for topic_name, topic_admin in topics.items():
                    self.create_topic(topic_admin, topic_name)
        except FileNotFoundError:
            with open(self.__topicsFile, "w") as topicsFile:
                topicsFile.write("{}")

    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, id: UserId, topicname: str) -> Topic:
        """
        Dado um usuário e o nome de tópico que deseja-se criar, o tópico é criado, caso já não exista.
        O criador do tópico é automaticamente subscrito no novo tópico criado.
        """
        if topicname not in self.topics:
            self.topics[topicname] = [id]
        if id not in self.users:
            self.users[id] = UserInfo(
                online=False, callback=lambda: None, messages_queue=[]
            )

        return Topic(topicname)


class BrokerService(rpyc.Service):  # type: ignore
    def __init__(self, brokerData):
        """
        Construtor chamado a cada conexão no threaded server. Usa o brokerData como estrutura de dados
        compartilhado entre cada instância.
        """
        self.data = brokerData
        self.client_conn = None

    def on_connect(self, conn):
        client_ip = conn._channel.stream.sock.getpeername()[0]
        print(f"Conexao iniciada: {client_ip}")
        self.data.connections[conn] = None
        self.client_conn = conn

    def on_disconnect(self, conn):
        if self.data.connections[conn] != None:
            print(f"{self.data.connections[conn]} finalizou a conexão.")
            self.data.users[conn].online = False
            self.data.users[conn].FnNotify = None
        del self.data.users[conn]
        del self.data.connections[conn]

    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, id: UserId, topicname: str) -> Topic:
        """
        Dado um usuário e o nome de tópico que deseja-se criar, o tópico é criado, caso já não exista.
        O criador do tópico é automaticamente subscrito no novo tópico criado.
        """
        if topicname not in self.data.topics:
            self.data.topics[topicname] = [id]
        if id not in self.data.users:
            self.data.users[id] = UserInfo(
                online=False, callback=lambda: None, messages_queue=[]
            )

        return Topic(topicname)

    # Handshake
    def exposed_login(self, id: UserId, callback: FnNotify) -> bool:
        """
        Dado um usuário, registra sua função de callback para envio de mensagens, e o ativa como online.
        Caso existam mensagens que chegaram enquanto o usuário estava offline, essas mensagens serão encaminhadas ao usuário.
        """
        self.data.connections[self.client_conn] = id
        if id not in self.data.users:
            print(f"Novo usuário: {id}")
            self.data.users[id] = UserInfo(
                online=True, callback=callback, messages_queue=[]
            )
        else:
            print(f"Usuário se reconectou: {id}")
            self.data.users[id].online = True
            self.data.users[id].callback = callback
            if len(self.data.users[id].messages_queue) > 0:
                callback(self.data.users[id].messages_queue)
        return True

    def exposed_list_topics(self) -> list[Topic]:
        """
        Retorna todos os tópicos cadastrados no broker.
        """
        return list(self.data.topics.keys())

    # Publisher operations
    def exposed_publish(self, id: UserId, topic: Topic, data: str) -> bool:
        """
        Função responde se Anúncio conseguiu ser publicado.
        """
        print(f"{id} está publicando no tópico {topic}.")
        if topic in self.data.topics:
            print(f"Usuários inscritos em {topic}: {self.data.topics[topic]}")
            for user in self.data.topics[topic]:
                content = Content(author=id, topic=topic, data=data)
                if self.data.users[user].online:
                    print(f"{user} está online. Chamando callback.")
                    self.data.users[user].callback([content])
                else:
                    print(f"{user} está offline. Enfileirando callback.")
                    self.data.users[user].messages_queue.append(content)
            return True
        return False

    # Subscriber operations
    def exposed_subscribe_to(self, id: UserId, topic: Topic) -> bool:
        """
        Função responde se `id` está inscrito no `topic`
        """
        if topic in self.data.topics:
            if id in self.data.users:
                if id not in self.data.topics[topic]:
                    print(f"{id} se inscreveu no tópico {topic}")
                    self.data.topics[topic].append(id)
                return True
        return False

    def exposed_unsubscribe_to(self, id: UserId, topic: Topic) -> bool:
        """
        Função responde se `id` não está inscrito no `topic`
        """
        if topic in self.data.topics:
            if id in self.data.users:
                if id in self.data.topics[topic]:
                    print(f"{id} se desinscreveu no tópico {topic}")
                    self.data.topics[topic].remove(id)
                return True
        return False


# dispara o servidor
if __name__ == "__main__":
    brokerData = BrokerData()
    service = classpartial(BrokerService, brokerData)
    srv = ThreadedServer(
        service,
        port=PORT,
        protocol_config={"allow_public_attrs": True},
    )
    print("Iniciando Servidor do Broker...")
    srv.start()
