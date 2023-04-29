# Laboratório 2
**Aplicação cliente/servidor básica**
**Sistemas Distribuı́dos (ICP-367 e MAB-733)**
**Prof. Silvana Rossetto**

**Instituto de Computação/UFRJ**

## Introdução
O objetivo deste Laboratório é desenvolver uma aplicação distribuída para aplicar os
conceitos estudados sobre arquitetura de software e arquitetura de sistema; servidores
multiplexados e concorrentes; e seguir praticando com a programação usando sockets.

A aplicação que vamos desenvolver será um **dicionário remoto** que poderá ser
consultado e alterado. As chaves e valores do dicionário serão strings. O dicionário
deverá ser armazenado em disco para ser restaurado em execução futura.

- Para a **consulta**, o usuário informará uma **chave** e receberá como resposta a
**lista de valores** associados a essa chave, em ordem alfabética (lista vazia caso
a entrada não exista).
- Para a **escrita** o usuário informará um par **chave e valor** e receberá como
resposta a confirmação que a nova entrada foi inserida, ou que o valor foi acrescentado
em uma entrada existente.
- A remoção de uma entrada no dicionário somente poderá ser feita pelo **administrador**
do dicionário.

## Atividade 1
**Objetivo**: Projetar a **arquitetura de software** da solução. A arquitetura de
software deverá conter, no mínimo, três componentes distintos: (i) acesso e persistência
de dados; (ii) processamento das requisições; e (iii) interface com usuário.

**Roteiro**: 

1. Escolha o **estilo arquitetural** para servir de base para o desempenho da
arquitetura de software.
2. Descreva os **componentes**, com suas **funcionalidades** (providas e usadas) e
modo de **conexão** entre eles.

## Atividade 2
**Objetivo**: Instanciar a arquitetura de software da aplicação (definida na
Atividade 1) para uma **arquitetura de sistema cliente/servidor** de dois níveis, com
um servidor e um cliente. O lado do servidor abrigará um dicionário remoto, enquanto
o lado cliente ficará responsável pela interface com o usuário.

**Roteiro**:

1. Implemente o código do lado cliente e do lado servidor;
2. Modularize o código de forma concisa e clara;
3. Experimente a aplicação usando diferentes casos de teste.
4. Reporte as decisões tomadas em todas as Atividades no README do repositório do
código.

O servidor deverá ser **multiplexado**: capaz de receber comandos básicos da entrada
padrão (inclua comandos para permitir finalizar o servidor quand não houver clientes
ativos e remover uma entrada do dicionário). **Use a função select**.

O servidor deverá ser **concorrente**: deverá tratar cada nova conexão de cliente como
um novo fluxo de execução e atender as requisições desse cliente dentro do novo fluxo
de execução. **Crie threads ou processos filhos**.

**Disponibilize seu código**

Disponibilize seu código Disponibilize o código da sua aplicação em um ambiente de
acesso remoto (GitHub ou GitLab) e use o formulário de entrega do laboratório para
encaminhar as informações solicitadas.
