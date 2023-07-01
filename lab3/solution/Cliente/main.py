import sys
import rpyc

SERVIDOR = "localhost"
PORTA = 3000


class InterfaceCliente(object):
    def __init__(self, conn):
        self.__conn = conn
        self.__comandos = {
            "ler": {
                "sintaxe_esperada": "ler <chave>",
                "descricao": "Lê uma chave do dicionário remoto.",
            },
            "escrever": {
                "sintaxe_esperada": "escrever <chave> <valor>",
                "descricao": "Escreve o valor em uma chave do dicionário remoto.",
            },
            "remover": {
                "sintaxe_esperada": "remover <chave>",
                "descricao": "Remove uma chave do dicionário remoto.",
            },
            "ajuda": {
                "sintaxe_esperada": "ajuda <comando>",
                "descricao": "Obtem informações acerca de um comando.",
            },
            "sair": {
                "sintaxe_esperada": "sair",
                "descricao": "Encerra a execução do cliente.",
            },
        }

    def cumprimentar(self):
        welcome_str = """
       .--.                   .---.
   .---|__|           .-.     |~~~|
.--|===|--|_          |_|     |~~~|--.          Dicionário Remoto
|  |===|  |'\     .---!~|  .--|   |--|       
|%%|   |  |.'\    |===| |--|%%|   |  |       - ler <chave>
|%%|   |  |\.'\   |   | |__|  |   |  |       - escrever <chave> <valor>
|  |   |  | \  \  |===| |==|  |   |  |       - remover <chave>
|  |   |__|  \.'\ |   |_|__|  |~~~|__|       - ajuda <comando>
|  |===|--|   \.'\|===|~|--|%%|~~~|--|       - sair
^--^---'--^    `-'`---^-^--^--^---'--'       - para listar os comandos novamente, digite "ajuda"
"""
        print(welcome_str)

    def executar_comando(self, input_str):
        comando_inteiro = input_str.split(" ")
        comando_nome = comando_inteiro[0]
        comando_args = comando_inteiro[1:]

        if comando_nome in self.__comandos.keys():
            func = getattr(self, comando_nome)
            func(comando_args)
        else:
            print(
                f"Comando invalido: {comando_nome}. Use algum dos seguintes: {list(self.__comandos.keys())}"
            )
        print()

    def ajuda(self, comando_args):
        if len(comando_args) == 1 and comando_args[0] in self.__comandos.keys():
            comando = comando_args[0]
            print(f"Comando: {comando}")
            print(f"Sintaxe esperada:", self.__comandos[comando]["sintaxe_esperada"])
            print(f"Descrição:", self.__comandos[comando]["descricao"])
        else:
            print("Comandos disponíveis: ", list(self.__comandos.keys()))
            print(
                "Digite 'ajuda <comando>' para obter mais informações acerca de um comando específico."
            )

    def ler(self, comando_args):
        if len(comando_args) != 1:
            print(f"Sintaxe esperada: ", {self.__comandos["ler"]["sintaxe_esperada"]})
            return
        chave = comando_args[0]
        print(f"Lendo '{chave}'...")
        valor = self.__conn.root.exposed_ler(chave)
        if valor is None:
            print("[]")
        else:
            print(valor)

    def escrever(self, comando_args):
        if len(comando_args) < 2:
            print(
                f"Sintaxe esperada: ", {self.__comandos["escrever"]["sintaxe_esperada"]}
            )
            return
        chave, valor = comando_args[0], " ".join(comando_args[1:])
        print(f"Escrevendo [{chave}: {valor}]...")
        retorno = self.__conn.root.exposed_escrever(chave, valor)
        print(retorno)

    def remover(self, comando_args):
        if len(comando_args) != 1:
            print(
                f"Sintaxe esperada: ", {self.__comandos["remover"]["sintaxe_esperada"]}
            )
            return
        chave = comando_args[0]
        print(f"Removendo '{chave}'...")
        retorno = self.__conn.root.exposed_remover(chave)
        print(retorno)

    def sair(self, comando_args):
        if len(comando_args) != 0:
            print(f"Sintaxe esperada: ", {self.__comandos["sair"]["sintaxe_esperada"]})
            return
        self.__conn.close()
        sys.exit()


def iniciaConexao():
    conn = rpyc.connect(SERVIDOR, PORTA)
    return conn


def main():
    conn = iniciaConexao()
    interface = InterfaceCliente(conn)

    interface.cumprimentar()
    while True:
        input_str = input()
        interface.executar_comando(input_str)


# executa o cliente
if __name__ == "__main__":
    main()
