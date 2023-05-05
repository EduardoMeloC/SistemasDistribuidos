from Dominio.IDicionario import IDicionario
from Dominio.IRepositorio import IRepositorio

class ServicoDicionario(object):
    def __init__(self, dicionario: IDicionario, repositorio: IRepositorio):
        self.__dicionario = dicionario
        self.__repositorio = repositorio
    
    def ler(self, chave):
        return self.__dicionario.ler(chave)

    def escrever(self, chave, valor):
        self.__dicionario.escrever(chave, valor)

    def apagar(self, chave):
        self.__dicionario.apagar(chave)

    def salvar(self):
        self.__repositorio.salvar(self.__dicionario)

    def carregar(self):
        dicionario_carregado = self.__repositorio.carregar()
        for key, value_list in dicionario_carregado.items():
            for value in value_list:
                self.__dicionario.escrever(key, value)

