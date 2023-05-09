## Comunicação do Dicionário

Neste módulo, foram criadas funções para auxiliar os servidores e os clientes para criação de mensagens que tivessem a semântica de "requisição" e "resposta", inspirando-se no protocolo HTTP. Dessa maneira, é possível realizar requisições do tipo ```get```, ```post```, ```delete``` ou ```action```, e combinando cada um desses tipos de requisições com seus parâmetros, é possível que o servidor escolha o serviço mais adequado para a mensagem de acordo com a sua semântica.

No contexto do dicionário, o ```get``` é utilizado para a leitura, o ```post``` para escrita, o ```delete``` para remoção de chaves (embora não tenha sido implementado, dado que esta funcionalidade está somente no servidor - que já consegue invocar o serviço diretamente), e, o ```action``` para invocar uma função que não acessa um recurso, como carregar e salvar.

Quando o cliente digita algo como "ler a", é criada a seguinte mensagem, como uma request ao servidor:

```json
{
  "tipo": "get",
  "params": {"chave": "a"}
}
```

Em seguida, o servidor invoca o método de leitura do dicionário, e, se tudo ocorreu como esperado, a resposta é enviada ao cliente:

```json
{
  "tipo": "sucesso", 
  "corpo": {"valor": ["abacate", "acerola"]}
}

O cliente então conseguirá exibir diferentes resultados dependendo do tipo da resposta, e dependendo do seu valor.
É válido ressaltar que, mesmo seguindo um padrão para a comunicação, é importante conhecer quais são as chaves que serão enviadas no "corpo" da resposta - esse detalhe não é do escopo do módulo de comunicação, mas do contrato entre o cliente e servidor, e o que cada um espera de suas
requisições e suas respostas.

}

