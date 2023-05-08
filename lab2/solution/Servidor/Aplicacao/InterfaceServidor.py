import sys
from Dominio.ServicoDicionario import ServicoDicionario

class InterfaceServidor(object):
    def __init__(self, servico_dicionario: ServicoDicionario, conexoes_ativas):
        self.__servico_dicionario = servico_dicionario
        self.__conexoes_ativas = conexoes_ativas

    def set_socket(self, server_socket):
        self.__server_socket = server_socket
    
    def executar_comando(self, input_str):
        comando_inteiro = input_str.split(" ")
        comando_nome = comando_inteiro[0]
        comando_args = comando_inteiro[1:]
        
        comandos_disponiveis = ["ler", "escrever", "apagar", "salvar", "carregar", "desligar", "listarconexoes"]
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
        valor = self.__servico_dicionario.ler(chave)
        if valor == None:
            print("Nenhum valor encontrado.")
        else:
            print(valor)
    
    def escrever(self, comando_args):
        if len(comando_args) != 2:
            print(f"Sintaxe esperada: escrever <chave> <valor>")
            return
        chave, valor= comando_args[0], comando_args[1]
        print(f"Escrevendo [{chave}: {valor}]...")
        self.__servico_dicionario.escrever(chave, valor)

    def apagar(self, comando_args):
        if len(comando_args) != 1:
            print(f"Sintaxe esperada: apagar <chave>")
            return
        chave = comando_args[0]
        print(f"Apagando {chave}...")
        self.__servico_dicionario.apagar(chave)
    
    def carregar(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: carregar")
            return
        print("Carregando...")
        self.__servico_dicionario.carregar()

    def salvar(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: salvar")
            return
        print("Salvando...")
        self.__servico_dicionario.salvar()

    def desligar(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: desligar")
            return
        if not self.__conexoes_ativas:
            self.__server_socket.close()
            sys.exit()
        else:
            print("Ha conexoes ativas.")

    def listarconexoes(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: listarconexoes")
            return
        print(self.__conexoes_ativas)

