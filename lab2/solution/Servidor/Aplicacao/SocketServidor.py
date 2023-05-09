import socket
import select
import sys
import threading

from Aplicacao.Endpoints import Endpoints
from Dominio.ServicoDicionario import ServicoDicionario
from Aplicacao.InterfaceServidor import InterfaceServidor

class SocketServidor(object):
    def __init__(self, servico_dicionario: ServicoDicionario, configuracao):
        self.__endpoints = Endpoints(servico_dicionario)
        self.__port = configuracao["porta"]
        self.__host = ''
        self.__lock = threading.Lock()
        self.__conexoes_ativas = {}
        self.__threads_de_cliente = []
        self.__entradas_do_select = [sys.stdin]
        self.__interface_servidor = InterfaceServidor(servico_dicionario, self.__conexoes_ativas, self.__threads_de_cliente)

    def __inicia_servidor(self):
        #Internet( IPv4, + TCP )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.__host, self.__port))
        sock.listen(5)
        sock.setblocking(False)
        self.__interface_servidor.set_socket(sock)
        return sock

    def __aceita_conexao(self, sock):
        client_socket, client_address = sock.accept()
        return client_socket, client_address

    def __atende_requisicoes(self, client_socket, client_address):
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(str(client_address) + '-> encerrou')
                self.__lock.acquire()
                self.__conexoes_ativas.pop(client_socket)
                self.__lock.release()
                client_socket.close()
                return
            print(str(client_address) + ': ' + str(data, encoding='utf-8'))
            response = self.__endpoints.processar_mensagem(data)
            client_socket.send(response)

    def run(self):
        server_socket = self.__inicia_servidor()
        print('Pronto para receber conexoes...')
        self.__entradas_do_select.append(server_socket)
        while True:
            r, w, e = select.select(self.__entradas_do_select, [], [])
            for pronto in r:
                if pronto == server_socket:
                    client_socket, client_address = self.__aceita_conexao(server_socket)
                    print('Conectado com: ', client_address)
                    self.__lock.acquire()
                    self.__conexoes_ativas[client_socket] = client_address
                    self.__lock.release()
                    cliente_thread = threading.Thread(target=self.__atende_requisicoes, args=(client_socket, client_address))
                    cliente_thread.start()
                    self.__threads_de_cliente.append(cliente_thread)
                elif pronto == sys.stdin:
                    user_input = input()
                    self.__interface_servidor.executar_comando(user_input)