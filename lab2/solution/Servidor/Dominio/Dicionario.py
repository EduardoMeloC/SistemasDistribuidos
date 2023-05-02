from solution.Servidor.Dominio.IDicionario import IDicionario

class Dicionario(IDicionario):
    def __init__(self):
        self.__dicionario = dict()

    def ler(self, chave):
        if chave in self.__dicionario:
            valor = self.__dicionario.get(chave)
            return valor
        else:
            return None


    def escrever(self, chave, valor):
        if chave not in self.__dicionario:
            self.__dicionario[chave] = {}
        self.__dicionario[chave].append(valor)

    def apagar(self, chave):
        if chave in self.__dicionario:
            self.__dicionario[chave] = {}