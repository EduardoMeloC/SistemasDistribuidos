import json

def criar_mensagem(tipo, params):
    """
    Cria uma mensagem para estabelecer a comunicação sobre a camada de trasporte.

    Args:
        tipo (str): o tipo da request ('get', 'post', 'delete' ou 'action')
        params (dict): os parâmetros da request
    """

    tipos_disponiveis = ['get', 'post', 'delete', 'action']
    if tipo not in tipos_disponiveis:
        raise ValueError(f'recebeu {tipo} na mensagem, mas esperava algum entre {tipos_disponiveis}')
    if not isinstance(params, dict):
        raise ValueError(f'params deveria ser um {type(dict)}, mas recebeu um {type(params)}')

    mensagem = {
        "tipo": tipo,
        "params": params
    }
    return json.dumps(mensagem).encode()

def ler_mensagem(message_bytes):
    """
    Lê uma mensagem enviada e a transforma no objeto se seguir à especificação.

    Args:
        message_bytes (bytes): sequência de bytes da mensagem contendo {tipo, params}
    """
    try:
        mensagem = json.loads(message_bytes.decode())
    except:
        raise ValueError(f'A mensagem não possui o formato adequado')
    if "tipo" not in mensagem:
        raise ValueError(f'A mensagem lida não possui tipo')
    if "params" not in mensagem:
        raise ValueError(f'A mensagem lida não possui params')

    tipo, params = mensagem['tipo'], mensagem['params']
    tipos_disponiveis = ['get', 'post', 'delete', 'action']
    if tipo not in tipos_disponiveis:
        raise ValueError(f'recebeu {tipo} na mensagem, mas esperava algum entre {tipos_disponiveis}')
    if not isinstance(params, dict):
        raise ValueError(f'params deveria ser um {type(dict)}, mas recebeu um {type(params)}')

    return mensagem