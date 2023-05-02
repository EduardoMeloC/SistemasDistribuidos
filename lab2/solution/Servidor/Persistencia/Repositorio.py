from solution.Servidor.Dominio.IRepositorio import IRepositorio
import json

class Repositorio(IRepositorio):
    def __init__(self, configuracao):
        self.__dbfile = configuracao["arquivo_de_persistencia"]

    def carregar_dicionario(self):
        with open(self.__dbfile, "r") as arquivo: 
            dicionario_carregado = json.load(arquivo)
            return dicionario_carregado

    def salvar_dicionario(self, dicionario):
        json_str = json.dumps(dicionario)
        with open(self.__dbfile, "w") as arquivo:
            arquivo.write(json_str)