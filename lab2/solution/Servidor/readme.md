## Servidor do Dicionário

Nesta instância da arquitetura de software, o servidor é responsável pelas implementações dos componentes de aplicação, domínio e persistência.

Durante a execução, o servidor pode executar uma série de comandos para a manipulação do dicionário, incluindo funções não disponíveis na aplicação do cliente (como desligar o servidor, listar conexões ativas e apagar uma chave do dicionário).

O arquivo main.py lê as configurações especificadas no arquivo ```settings.json```, como a porta que o servidor deverá utilizar, e qual arquivo será utilizado como "banco de dados" do servidor. Em seguida, ele instancia o serviço de dicionário e executa o loop principal do socket.

Ao executar o servidor, inicialmente o dicionário estará vazio. Para carregar os dados da base, é possível executar o comando ```carregar```, e esse comando mesclará o dicionário da execução atual com o dicionário da base de dados. É válido ressaltar que clientes também podem executar essa função, mas, na prática, ela só precisa ser executada uma vez.

### Camada de Domínio

- A camada de domínio expõe duas interfaces: ```IDicionario``` (criando um contrato para as funções ```ler```, ```escrever``` e ```apagar```) e ```IRepositorio``` (criando um contrato para as funções de ```salvar``` e ```carregar```).
- A interface ```IDicionario``` é implementada nesta própria camada, na classe ```Dicionario```. Nesta implementação, o dicionário possui strings como chaves e listas de strings como valores. Cada inserção é feita de maneira ordenada na lista utilizando ```bisect.insort```, e apagar um elemento apaga toda a lista.
- O ```ServicoDicionario``` é uma classe que une o ```Dicionario``` e o ```Repositorio```, expondo os métodos de cada uma dessas classes para a camada de aplicação.
- Ao executar a função de ```carregar```, o retorno será somente o dicionário persistido. O serviço é responsável por mesclar o dicionário existente da execução atual pelo dicionário carregado da persistência.

### Camada de Persistência

- A camada de persistência possui uma classe ```Repositorio``` que implementa a interface ```IRepositorio``` especificada na camada de domínio. Nesta implementação, as operações de ```salvar``` e ```carregar``` operam sobre o arquivo especificado em ```settings.json```, sob a chave ```arquivo_de_persistencia``` (no caso, o arquivo ```db.json```).
- Os dados do dicionário são guardados no formato .json

### Camada de Aplicação

A camada de aplicação possui três classes:

- **Endpoints -** Responsável por ler os bytes de uma request enviada pelo cliente com o auxílio da função ```ler_request``` criada no módulo de Mensagem. Ao ler a request, é necessário verificar qual é o "tipo" da request ('get', 'post' ou 'action') e seus parâmetros com a finalidade de invocar o serviço de dicionário da maneira adequada. Após chamar um serviço, é enviada uma resposta ao cliente com o auxílio da função ```criar_response```, também definida no módulo de Mensagem.
- **InterfaceServidor -** Dada uma string digitada pelo servidor no stdin, a interface do servidor é responsável pela leitura dessa string e exibir a saída apropriada invocando o serviço de dicionário quando apropriado.
- **SocketServidor -** Responsável pela criação do socket TCP e realizar a multiplexação da entrada com a recepção de novos clientes, bem como a criação de novas threads para cada o atendimento das requisições de cada um dos clientes. Quando o servidor atende à requisição de um cliente, ele invoca a função ```processar_mensagem``` definida na classe de ```Endpoints```. Quando o servidor insere um novo comando no ```stdin```, o comando é enviado para a função ```executar_comando``` definida na classse ```InterfaceServidor```.