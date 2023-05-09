import os
import sys

# Get the path of the solution directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
solution_dir = os.path.dirname(parent_dir)
sys.path.append(solution_dir)

from Comunicacao.Mensagem import criar_request, ler_response

class Endpoints(object):
    def __init__(self, client_socket):
        self.__client_socket = client_socket

    def __enviar_request(self, request):
        self.__client_socket.send(request)
        responsebytes = self.__client_socket.recv(1024)
        response = ler_response(responsebytes)
        return response

    def ler(self, chave):
        request = criar_request('get', {'chave': chave})
        response = self.__enviar_request(request)
        return response

    def escrever(self, chave, valor):
        request = criar_request('post', {'chave': chave, 'valor': valor})
        response = self.__enviar_request(request)
        return response

    def salvar(self):
        request = criar_request('action', {'action': 'salvar'})
        response = self.__enviar_request(request)
        return response

    def carregar(self):
        request = criar_request('action', {'action': 'carregar'})
        response = self.__enviar_request(request)
        return response
