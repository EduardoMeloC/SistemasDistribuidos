from Dominio.IRepositorio import IRepositorio
from Dominio.Dicionario import Dicionario
import json

class Repositorio(IRepositorio):
    def __init__(self, configuracao):
        self.__dbfile = configuracao["arquivo_de_persistencia"]

    def salvar(self, dicionario: Dicionario):
        json_str = json.dumps(dicionario.underlying_dict)
        with open(self.__dbfile, "w") as arquivo:
            arquivo.write(json_str)
            
    def carregar(self):
        with open(self.__dbfile, "r") as arquivo: 
            dicionario_carregado = json.load(arquivo)
            return dicionario_carregado
