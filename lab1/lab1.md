# Laboratório 1
## Introdução à programação com sockets
## Sistemas Distribuı́dos (ICP-367 e MAB-733)
## Prof. Silvana Rossetto

## Instituto de Computação/UFRJ

## Introdução
O objetivo deste Laboratório é introduzir a programação com sockets usando a linguagem Python.
O módulo socket de Python provê acesso à interface Socket POSIX. A função
socket() retorna um objeto cujos métodos implementam as chamadas de sistema de
socket.

## Atividade 1
**Objetivo**: Desenvolver uma aplicação distribuı́da básica usando o modelo de interação
requisição/resposta (ou modo ativo/passivo).
**Roteiro**: A aplicação será um “servidor de echo”, que envia de volta para o emissor a
mesma mensagem recebida.
1. Implemente o **lado passivo** (“servidor de echo”) que coloca-se em modo de espera por conexões, recebe a mensagem do lado ativo e a envia de volta, e repete
esse procedimento até que o lado ativo encerre a conexão. Quando a conexão for
encerrada, o lado passivo deverá finalizar sua execução.
2. Implemente o **lado ativo** que conecta-se com o “servidor de echo” (lado passivo),
envia uma mensagem digitada pelo usuário, aguarda e imprime a mensagem recebida de volta.
3. Use a string ’fim’ como comando para o usuário indicar que não deseja mais enviar mensagens para o servidor de echo. Quando esse comando for digitado pelo
usuário, a conexão deverá ser fechada e a aplicação encerrada. Não é necessário
enviar o comando para o lado passivo.
4. Experimente sua aplicação executando os processos passivo e ativo em terminais
(janelas) distintos na mesma máquina (ou em máquinas distintas quando possı́vel).
Disponibilize seu código Disponibilize o código da sua aplicação em um ambiente de
acesso remoto (GitHub ou GitLab) e use o formulário de entrega do laboratório para
encaminhar as informações solicitadas.

Disponibilize seu código Disponibilize o código da sua aplicação em um ambiente de
acesso remoto (GitHub ou GitLab) e use o formulário de entrega do laboratório para
encaminhar as informações solicitadas.