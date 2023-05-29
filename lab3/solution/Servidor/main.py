# Ver documentação em: https://rpyc.readthedocs.io/en/latest/
import rpyc
import bisect
import json

from rpyc.utils.server import ThreadedServer

PORTA = 3000

class Dicionario(rpyc.Service):
    def __init__(self):
        self.__dbfile = "db.json"

    def salvar(self, db_dict):
        json_str = json.dumps(db_dict)
        with open(self.__dbfile, "w") as arquivo:
            arquivo.write(json_str)
            
    def carregar(self):
        try:
            with open(self.__dbfile, "r") as arquivo: 
                dicionario_carregado = json.load(arquivo)
                return dicionario_carregado
        except FileNotFoundError:
            with open(self.__dbfile, "w") as arquivo:
                arquivo.write("{}")
            return {}


    def on_connect(self, conn):
        client_ip = conn._channel.stream.sock.getpeername()[0]
        print(f"Conexao iniciada: {client_ip}")

    def on_disconnect(self, conn):
        client_ip = conn._channel.stream.sock.getpeername()[0]
        print(f"Conexao finalizada: {client_ip}")

    def exposed_ler(self, chave):
        db_dict = self.carregar()
        if chave in db_dict:
            valor = db_dict.get(chave)
            return valor
        else:
            return None

    def exposed_escrever(self, chave, valor):
        db_dict = self.carregar()
        is_nova_chave = False
        # Se não existe essa chave no dicionario, cria nova lista
        if chave not in db_dict:
            db_dict[chave] = []
            is_nova_chave = True
        # Se esse valor já não existe no dicionário, insere-o ordenadamente
        if valor not in db_dict[chave]:
            print("inserindo ", valor)
            bisect.insort(db_dict[chave], valor)
            print(db_dict[chave])
        self.salvar(db_dict)
        return "Nova chave inserida." if is_nova_chave else "Novo valor acrescentado à chave existente."

    def exposed_remover(self, chave):
        db_dict = self.carregar()
        if chave in db_dict:
            db_dict.pop(chave)
            self.salvar(db_dict)
            return "Chave removida com sucesso."
        else:
            return "Chave inexistente."


# dispara o servidor
if __name__ == "__main__":
    srv = ThreadedServer(Dicionario, port=PORTA)
    srv.start()
