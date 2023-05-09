import json

from Interface.SocketCliente import SocketCliente

arquivo_de_configuracoes = './settings.json'

def carregar_configuracao():
    with open(arquivo_de_configuracoes, 'r') as arquivo:
        configuracoes = json.load(arquivo)
        return configuracoes

def main():
    configuracao = carregar_configuracao()
    socketServidor = SocketCliente(configuracao)
    socketServidor.run()

if __name__ == '__main__':
    main()