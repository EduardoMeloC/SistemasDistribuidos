from Comunicacao.Mensagem import criar_mensagem

def ler(chave):
    return criar_mensagem('get', {'chave': chave})

def escrever(chave, valor):
    return criar_mensagem('post', {'chave': chave, 'valor': valor})

def salvar():
    return criar_mensagem('action', {'action': 'salvar'})

def carregar():
    return criar_mensagem('action', {'action': 'carregar'})
