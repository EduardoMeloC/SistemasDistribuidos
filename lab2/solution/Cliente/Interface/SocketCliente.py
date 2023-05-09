# Client

import socket

from Interface.InterfaceCliente import InterfaceCliente

class SocketCliente(object):
    def __init__(self, configuracao):
        self.__interface_cliente = InterfaceCliente()
        self.__host = 'localhost'
        self.__port = configuracao["porta"]
    
    def __inicia_cliente(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__host, self.__port))
        self.__interface_cliente.set_socket(sock)
        return sock

    def run(self):
        client_socket = self.__inicia_cliente()
        print('Conectado ao servidor de dicionário')
        while True:
            user_input = input()
            self.__interface_cliente.executar_comando(user_input)
