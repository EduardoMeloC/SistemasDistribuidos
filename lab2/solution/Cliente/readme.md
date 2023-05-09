## Cliente do Dicionário

Nesta instância da arquitetura de software, o cliente é responsável pela implementação do componente de Interface.

Durante a execução, o cliente pode executar uma série de comandos para a manipulação do dicionário remoto, como ```ler```, ```escrevrer```, ```carregar```, ```salvar``` e ```sair```

O arquivo main.py lê as configurações especificadas no arquivo ```settings.json```, como a porta que o servidor deverá utilizar. Em seguida, ele instancia o socket e executa seu loop principal.

Ao executar um cliente, é possível que o dicionário não contenha os dados que foram persistidos na base de dados do servidor (o arquivo "db.json"). Para carregar os dados da base, é possível executar o comando ```carregar```, e esse comando mesclará o dicionário da execução atual com o dicionário da base de dados. É válido ressaltar que embora vários clientes possam executar essa função, na prática, ela só precisa ser executada uma vez desde o primeiro momento em que o servidor foi levantado.

### Camada de Interface

A camada de interface possui três classes:

- **Endpoints -** Responsável por criar uma request o auxílio da função ```criar_request``` criada no módulo de Mensagem. Ao criar a request, a mensagem da requisição é enviada ao servidor e em seguida o servidor envia uma resposta, que pode indicar se a nossa request foi executada com sucesso ou se ocorreu uma falha. Essa resposta é enviada como uma sequência de bytes que segue um formato específico, mas com o auxílio da função ```ler_response```, definida no módulo de Mensagem, é possível compreendê-la facilmente. Para cada um dos endpoints, é retornada essa ```response```.
- **InterfaceCliente -** Dada uma string digitada pelo cliente no stdin, a interface do cliente é responsável pela leitura dessa string e pela chamada do seu endpoint correspondente, que criará uma request e retornará uma response. Dependendo do resultado dessa response, diferentes saídas podem ser impressas ao usuário.
- **SocketServidor -** Responsável pela criação do socket TCP e realizar a conexão com o servidor. Quando o cliente insere um novo comando no ```stdin```, o comando é enviado para a função ```executar_comando``` definida na classse ```InterfaceCliente```.