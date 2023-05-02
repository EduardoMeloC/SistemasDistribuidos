import json

arquivo_de_configuracoes = './settings.json'
global configuracoes

def load_settings():
    with open(arquivo_de_configuracoes, 'r') as arquivo:
        configuracoes = json.load(arquivo)

def main():
    load_settings()
    print(configuracoes)
    pass

if __name__ == '__main__':
    main()