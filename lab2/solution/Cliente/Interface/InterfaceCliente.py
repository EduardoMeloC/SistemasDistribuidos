from Interface.Endpoints import Endpoints
import sys

class InterfaceCliente(object):
    def __init__(self):
        self.__endpoints = None
        self.__client_socket = None

    def set_socket(self, client_socket):
        self.__client_socket = client_socket
        self.__endpoints = Endpoints(client_socket)
    
    def executar_comando(self, input_str):
        comando_inteiro = input_str.split(" ")
        comando_nome = comando_inteiro[0]
        comando_args = comando_inteiro[1:]
        
        comandos_disponiveis = ["ler", "escrever", "salvar", "carregar", "sair"]
        if comando_nome in comandos_disponiveis:
            func = getattr(self, comando_nome)
            func(comando_args)
        else:
            print(f"Comando invalido: {comando_nome}. Use algum dos seguintes: {comandos_disponiveis}")

    def ler(self, comando_args):
        if len(comando_args) != 1:
            print(f"Sintaxe esperada: ler <chave>")
            return
        chave = comando_args[0]
        response = self.__endpoints.ler(chave)
        if response.get("tipo") == "sucesso":
            valor = response.get("corpo").get("valor")
            if valor == None:
                print("Nenhum valor encontrado.")
            else:
                print(valor)
        elif response.get("tipo") == "falha":
            print("Ocorreu um erro ao realizar a requisição.")

    def escrever(self, comando_args):
        if len(comando_args) != 2:
            print(f"Sintaxe esperada: escrever <chave> <valor>")
            return
        chave, valor = comando_args[0], comando_args[1]
        response = self.__endpoints.escrever(chave, valor)
        if response.get("tipo") == "sucesso":
            print(f"Escrevendo [{chave}: {valor}]...")
        elif response.get("tipo") == "falha":
            print("Ocorreu um erro ao realizar a requisição.")

    def carregar(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: carregar")
            return
        response = self.__endpoints.carregar()
        if response.get("tipo") == "sucesso":
            print(f"Carregando...")
        elif response.get("tipo") == "falha":
            print("Ocorreu um erro ao realizar a requisição.")

    def salvar(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: salvar")
            return
        response = self.__endpoints.salvar()
        if response.get("tipo") == "sucesso":
            print(f"Salvando...")
        elif response.get("tipo") == "falha":
            print("Ocorreu um erro ao realizar a requisição.")

    def sair(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: sair")
            return
        self.__client_socket.close()
        sys.exit()
