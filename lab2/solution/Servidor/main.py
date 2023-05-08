import json

from Dominio.Dicionario import Dicionario
from Dominio.ServicoDicionario import ServicoDicionario
from Persistencia.Repositorio import Repositorio
from Aplicacao.SocketServidor import SocketServidor

arquivo_de_configuracoes = './settings.json'

def carregar_configuracao():
    with open(arquivo_de_configuracoes, 'r') as arquivo:
        configuracoes = json.load(arquivo)
        return configuracoes

def main():
    configuracao = carregar_configuracao()
    servicoDicionario = ServicoDicionario(Dicionario(), Repositorio(configuracao))
    socketServidor = SocketServidor(servicoDicionario, configuracao)
    socketServidor.run()
    # servicoDicionario.escrever("a", "abacate")
    # servicoDicionario.escrever("b", "bergamota")
    # servicoDicionario.escrever("a", "acerola")
    # servicoDicionario.carregar()
    # print(servicoDicionario.ler("a"))
    # print(servicoDicionario.ler("b"))
    # servicoDicionario.salvar()

if __name__ == '__main__':
    main()