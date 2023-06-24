# Trabalho 1

**Aplicação distribuída de um sistema de anúncios**
**Sistemas Distribuı́dos (ICP-367 e MAB-733)**
**Prof. Silvana Rossetto**

**Instituto de Computação/UFRJ**

**Objetivo e tarefa**

O objetivo deste trabalho é projetar uma aplicação distribuída de 'anúncios' para aplicar os conceitos estudados até aqui.

O trabalho deverá ser feito preferencialmente em grupos de 3 alunos.

Para o contexto deste exercício, uma aplicação de anúncios é uma aplicação distribuída que permite que usuários publiquem, registrem interesse e recebam notificações de anúncios.

## Atividade 1

**Objetivo**: Descrever os requisitos gerais da aplicação.

Um usuário poderá: 1. criar e publicar anúncios; 2. registrar interesse em anúncios e ser notificado quando eles ocorrerem, mesmo que não esteja ativo ao mesmo tempo; 3. cancelar o registro de interesse em anúncios e não receber novas notificações;

## Atividade 2

**Objetivo**: Descrever a arquitetura de software da aplicação.

Adotaremos o estilo arquitetural publish-subscribe.
Os anúncios serão identificados por tópicos, contendo um conjunto de atributos.
Os componentes principais da aplicação são: 1. componente que publica anúncio (cria um anúncio e o envia para o gerente de anúncios) 2. componente que registra interesse em anúncio (registra interesse em um anúncio no gerente de anúncios e recebe notificação de anúncio) 3. componente de barramento ou gerente de anúncios (informa lista de tópicos de anúncios, cria um novo tópico (permitida apenas para o administrador), recebe anúncio para publicação, recebe subscrição de interesse, notifica componente que registrou interesse, armazena os anúncios até sua expiração)

**Especificar**:
Registro de subscriber: login (não permite mais de um usuário com o mesmo login)
Atributos de anúncio: tópico, autor, string com o conteúdo do anúncio  
Forma de entrega: notifica já enviando o conteúdo
Persistência e entrega a posteriori: como armazenar e como entregar para subscribers ativos a posteriori (na proxima conexao, recebe todos os anúncios anteriores)

## Atividade 3

**Objetivo**: Descrever a arquitetura de sistema da aplicação.

Adotaremos a arquitetura cliente-servidor (com um único servidor):
Os componentes de publicação e registro de interesse ficarão do lado cliente.
O componente gerente de anúncios ficará do lado servidor.

## Atividade 4

**Objetivo**: Descrever o protocolo de camada de aplicação

Alternativas:
usar camada de middleware RPC (RPyC)

## Atividade 5

**Objetivo**: Descrever decisões de implementação

Elencar outras decisões de implementação

## Atividade 6

**Objetivo**: Descrever a interface com o usuário

Cada grupo pode fazer a sua descrição.
