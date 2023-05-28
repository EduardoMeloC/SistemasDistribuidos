# Laboratório 3 
**Aplicação cliente/servidor básica**
**Sistemas Distribuı́dos (ICP-367 e MAB-733)**
**Prof. Silvana Rossetto**

**Instituto de Computação/UFRJ**

**Objetivo e tarefa**

O objetivo deste Laboratório é praticar a abstração de Chamada Remota de Procedimento (RPC).

Vamos reimplementar o dicionário remoto do Laboratório 2 (com algumas alterações, descritas abaixo), agora usando um middleware RPC (RPyC). As chaves e valores do dicionário serão strings. O dicionário deverá ser armazenado em disco para ser restaurado em uma execução futura.

O lado servidor da aplicação deverá oferecer as seguintes funcionalidades de um dicionário remoto:

- **consulta**: o usuário informará uma chave e receberá como resposta a lista de valores associados a essa chave, em ordem alfabética (lista vazia caso a entrada não exista).
- **escrita**: o usuário informará um par chave e valor e receberá como resposta a confirmação de que a nova entrada foi inserida ou que o novo valor foi acrescentado a uma entrada existente.
- **remoção**: o usuário informará uma chave e receberá como resposta a confirmação de que a entrada foi removida ou que se tratava de uma entrada inexistente.

As operações de escrita e remoção deverão ser salvas em disco de forma automática pelo servidor.

O servidor deverá ser multithreading: deverá tratar cada nova conexão de cliente como um novo fluxo de execução e atender às requisições desse cliente dentro do novo fluxo de execução.

O lado cliente deverá oferecer uma interface de acesso para as funcionalidades descritas acima.

**Disponibilize seu código**

Disponibilize o código da sua aplicação em um ambiente de acesso remoto (GitHub ou GitLab) e envie o link para a professora, usando o formulário de entrega desse laboratório.