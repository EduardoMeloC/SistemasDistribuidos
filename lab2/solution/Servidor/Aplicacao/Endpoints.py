import os
import sys

# Get the path of the solution directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
solution_dir = os.path.dirname(parent_dir)
sys.path.append(solution_dir)

from Comunicacao.Mensagem import ler_mensagem
from Dominio.ServicoDicionario import ServicoDicionario

class Endpoints(object):
    def __init__(self, servico_dicionario: ServicoDicionario):
        self.servico_dicionario = servico_dicionario

    def processar_mensagem(self, bytes_mensagem):
        mensagem = ler_mensagem(bytes_mensagem)
        tipo, params = mensagem['tipo'], mensagem['params']

        if tipo == 'get':
            if 'chave' not in params:
                raise ValueError(f"Esperava 'chave' como um parametro de get")
            chave = params['chave']
            return self.servico_dicionario.ler(chave)
        if tipo == 'post':
            if 'chave' not in params:
                raise ValueError(f"Esperava 'chave' como um parametro de post")
            if 'valor' not in params:
                raise ValueError(f"Esperava 'valor' como um parametro de post")
            chave, valor = params['chave'], params['valor']
            return self.servico_dicionario.escrever(chave, valor)
        if tipo == 'action':
            if 'action' not in params:
                raise ValueError(f"Esperava 'action' como um parametro de action")
            action = params['action']
            actions_disponiveis = ['salvar', 'carregar']
            if action not in actions_disponiveis:
                raise ValueError(f"Esperava parametro 'action' como algum entre: {actions_disponiveis}, mas recebeu {action}")
            if action == 'salvar':
                return self.servico_dicionario.salvar()
            if action == 'carregar':
                return self.servico_dicionario.carregar()