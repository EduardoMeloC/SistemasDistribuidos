# region imports, classes and aliases

from __future__ import annotations
import os
from rpyc.utils.server import ThreadedServer

# Se não funcionar no lab rode:
# $ pip install --user typing_extensions
import sys

IS_NEW_PYTHON: bool = sys.version_info >= (3, 10)
if IS_NEW_PYTHON:
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from typing import Callable, TYPE_CHECKING, List, Dict, Union
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

from simple_term_menu import TerminalMenu
from threading import Thread

SERVER = "localhost"
PORT = 10001


class UserInfo:
    def __init__(self, online: bool, callback: FnNotify, messages_queue: List[Content]):
        self.online = online
        self.callback = callback
        self.messages_queue = messages_queue


def iniciaConexao():
    conn = rpyc.connect(SERVER, PORT)
    return conn


class InterfaceCliente(object):
    def __init__(self, conn):
        self.__conn = conn
        self.username = None
        self.topics = self.__conn.root.exposed_list_topics()

    def cumprimentar(self):
        welcome_str_small = """
╔═══════════════════════════╗ 
║ CANAL DE ANÚNCIOS DA UFRJ ║
╚═══════════════════════════╝ 
"""
        welcome_str_big = """
            ,w═Q▄▄▄▄▄▄▄▄▄═∞,            
         »Q▄R██████████████▄▄╤                 ╔═══════════════════════════╗ 
      ,*▄▀███████▀▀▀▀▀▀███████▀▄▀,             ║ CANAL DE ANÚNCIOS DA UFRJ ║
     ƒ▄██████▀.²$▄█╩ⁿ▐██╨▄▄█████▀▄▀            ╚═══════════════════════════╝
    Ñ█████▀▀&╛--`▐┌ r¬√ █████████▄▀▀╕          - Listar topicos
   Ñ█████└√▄█╨,Ö~    ¿YD╜,@▄▌██████▀▐          - Publicar
  ▐█████▐/▄▓Ö╣║ Æ⌐═`,═`╓å@╫╢▓,╓████▌▌█         - Inscrever
  ▌████╠▌▄█W¢▓╨b╖,∩▄²╙▓▓▓▀╝║╜Q▄▄▄▄▄█▐▐         - Desinscrever
  Ü▌█▀>@ ▐██,`,═▄╔╦ ▀▄═$╤║,▄,█▀█████▐H▌        - Sair
  Ü▌█╔ ▌▌ ████$╬▌▌╠▓æ╬▒`   ¨ ▐██████j ▌ 
  ▌▌▌╝,   ▐███`▌Ü▌▀Q▀         ██▌███j ▌ 
Ç▒▌▌███ \╝]█▀╩&╝▓▐M ╘      ¬▄███████▐H▌▐
 ▓┐╠)╣█▌  ██▓▓D▐╢Æ         ,███▀██▌\▐├ ▐
 ╙U▐`╟██``▀▐▓▓▄▌▀      ╔█████▀   █╙╕ƒU▐ 
  ▐`Qk▌ ,,,▓╫Ü▌▌       ╠▀▄,,,,▄▄ⁿ╕▒CÜƒ  
 ▒,▀└╣W ═∞═╦▌╠ ^╥.*~, ▐╙╙╙▐▀▌███▌╬▒╛/▒Ö 
  ║╩╦╙▓  ,,▌╔¬▌╙╔▄▄ ^~~²╖W╦▌█▀▐/▌<╛▄▓▓  
 ╙══╧Ñ▒▒FH▌╝╠╠ƒ╔ⁿ⌐▄▌╚N⌐▓╣─D▓▓┌,╣M ▓#∞╚╙ 
     @╖▒'▀▐⌠B▐@▄▄▄╦k▀R▄⌐╬▌▄╩▓d▓,é▀#     
      ╙╩▀^═╣▓▄▓╫▓▐▌▌⌡▓Ü╖╬@╗▓▄M╩══╙      
           ▐▓▓▀▓▀▀╙▀▀▀▀▀▀▓▒▄║           
                 ╙▄▄▄▄╝            
"""
        columns, lines = os.get_terminal_size()
        if columns >= 96 and lines >= 21:
            print(welcome_str_big)
        else:
            print(welcome_str_small)

    def menu(self):
        options = {
            "Listar Tópicos": "listar_topicos",
            "Publicar": "publicar",
            "Inscrever": "inscrever",
            "Desinscrever": "desinscrever",
            "Sair": "sair",
        }
        options_list = list(options.keys())
        terminal_menu = TerminalMenu(options_list)
        selected_option_index = terminal_menu.show()
        selected_option = options_list[selected_option_index]
        option_function = getattr(self, options[selected_option])
        option_function()

    def listar_topicos(self):
        print("Esses são os tópicos que existem:")
        print(self.topics)

    def publicar(self):
        print("Em qual tópico você gostaria de publicar?")
        options = [*self.topics, "Topico Inexistente", "Cancelar"]
        terminal_menu = TerminalMenu(options)
        selected_topic_index = terminal_menu.show()
        selected_topic = options[selected_topic_index]
        if selected_topic == "Cancelar":
            return
        print("Digite a mensagem que gostaria de publicar:")
        message = input()
        if message != "":
            success = self.__conn.root.exposed_publish(
                self.username, selected_topic, message
            )
            if success:
                print("Mensagem publicada com sucesso.")
            else:
                print("Ocorreu um erro ao publicar a mensagem.")

    def inscrever(self):
        print("Em qual tópico você gostaria de se inscrever?")
        options = [*self.topics, "Topico Inexistente", "Cancelar"]
        terminal_menu = TerminalMenu(options)
        selected_topic_index = terminal_menu.show()
        selected_topic = options[selected_topic_index]
        if selected_topic == "Cancelar":
            return
        success = self.__conn.root.exposed_subscribe_to(self.username, selected_topic)
        if success:
            print(f"Você está inscrito no tópico {selected_topic}.")
        else:
            print(f"Ocorreu um erro ao se inscrever no tópico {selected_topic}.")

    def desinscrever(self):
        print("Em qual tópico você gostaria de se desinscrever?")
        options = [*self.topics, "Topico Inexistente", "Cancelar"]
        terminal_menu = TerminalMenu(options)
        selected_topic_index = terminal_menu.show()
        selected_topic = options[selected_topic_index]
        if selected_topic == "Cancelar":
            return
        success = self.__conn.root.exposed_unsubscribe_to(self.username, selected_topic)
        if success:
            print(f"Você não está inscrito no tópico {selected_topic}.")
        else:
            print(f"Ocorreu um erro ao se desinscrever no tópico {selected_topic}.")

    def sair(self):
        self.__conn.close()
        sys.exit()

    def callback(self, messages_queue: list[Content]):
        for content in messages_queue:
            author = content.author
            topic = content.topic
            data = content.data
            print(f"> {author} publicou no tópico {topic}:")
            print(data)

    def login(self):
        print("Usuário: ", end=None)
        self.username = input()
        successful_login = self.__conn.root.exposed_login(self.username, self.callback)
        if not successful_login:
            print("Usuário já existente com conexão ativa.")
            sys.exit()


def main():
    conn = iniciaConexao()
    interface = InterfaceCliente(conn)

    interface.cumprimentar()
    interface.login()

    while True:
        interface.menu()


# executa o cliente
if __name__ == "__main__":
    main()
