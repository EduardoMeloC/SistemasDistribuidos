from Dominio.IDicionario import IDicionario
from Dominio.IRepositorio import IRepositorio

from threading import Lock

class ServicoDicionario(object):
    def __init__(self, dicionario: IDicionario, repositorio: IRepositorio):
        self.__dicionario = dicionario
        self.__repositorio = repositorio
        self.__lock = Lock()
    
    def ler(self, chave):
        self.__lock.acquire()
        valor = self.__dicionario.ler(chave)
        self.__lock.release()
        return valor

    def escrever(self, chave, valor):
        self.__lock.acquire()
        self.__dicionario.escrever(chave, valor)
        self.__lock.release()

    def apagar(self, chave):
        self.__lock.acquire()
        self.__dicionario.apagar(chave)
        self.__lock.release()

    def salvar(self):
        self.__lock.acquire()
        self.__repositorio.salvar(self.__dicionario)
        self.__lock.release()

    def carregar(self):
        self.__lock.acquire()
        dicionario_carregado = self.__repositorio.carregar()
        for key, value_list in dicionario_carregado.items():
            for value in value_list:
                self.__dicionario.escrever(key, value)
        self.__lock.release()

