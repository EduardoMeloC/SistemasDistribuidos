from Dominio.IDicionario import IDicionario
import bisect

class Dicionario(IDicionario):
    def __init__(self):
        self.__dict = dict()

    def ler(self, chave):
        if chave in self.__dict:
            valor = self.__dict.get(chave)
            return valor
        else:
            return None

    def escrever(self, chave, valor):
        # Se não existe essa chave no dicionario, cria nova lista
        if chave not in self.__dict:
            self.__dict[chave] = []
        # Se esse valor já não existe no dicionário, insere-o ordenadamente
        if valor not in self.__dict[chave]:
            bisect.insort(self.__dict[chave], valor)

    def apagar(self, chave):
        if chave in self.__dict:
            self.__dict[chave] = {}

    @property
    def underlying_dict(self):
        return self.__dict