
# AWS Resource Management

Este projeto cria e gerencia recursos da AWS, incluindo buckets S3, tópicos SNS e filas SQS, DynamoDB.

## Pré-requisitos

- Python 3.x
- Boto3
- Credenciais AWS configuradas

## Instalação

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Instale as dependências:
    ```sh
    pip install boto3
    ```

3. Configure suas credenciais AWS:
    ```sh
    aws configure
    ```

## Uso

### Criar um Bucket S3

Execute o script `s3.py` para criar um bucket S3:
```sh
python 

s3.py


```

### Criar um Tópico SNS e Assinatura

Execute o script `sns.py` para criar um tópico SNS e uma assinatura de email:
```sh
python 

sns.py


```

### Criar uma Fila SQS e Assinar ao Tópico SNS

Execute o script `sqs.py` para criar uma fila SQS e assiná-la ao tópico SNS:
```sh
python 

sqs.py


```


### Criar uma Tabela DynamoDB

Execute o script `dynamodb.py` para criar uma tabela DynamoDB:
```sh
python 

dynamodb.py


```

### Inserir Nome do Arquivo e Quantidade de Linhas na Tabela DynamoDB

Execute o script `colocarArquivo.py` para listar os arquivos no bucket S3 e inserir o nome do arquivo e a quantidade de linhas na tabela DynamoDB:
```sh
python 

colocarArquivo.py


```

### Explicação

1. **Criar um Bucket S3**: Instruções para executar o script 

s3.py

 para criar um bucket S3.
2. **Criar um Tópico SNS e Assinatura**: Instruções para executar o script 

sns.py

 para criar um tópico SNS e uma assinatura de email.
3. **Criar uma Fila SQS e Assinar ao Tópico SNS**: Instruções para executar o script 

sqs.py

 para criar uma fila SQS e assiná-la ao tópico SNS.
4. **Criar uma Tabela DynamoDB**: Instruções para executar o script 

dynamodb.py

 para criar uma tabela DynamoDB.
5. **Inserir Nome do Arquivo e Quantidade de Linhas na Tabela DynamoDB**: Instruções para executar o script 

colocarArquivo.py

 para listar os arquivos no bucket S3 e inserir o nome do arquivo e a quantidade de linhas na tabela DynamoDB.

### Melhorias 

Criar a Função Lambda via Boto3: Atualmente, a função Lambda foi criada via console. Automatizar a criação da função Lambda usando Boto3 para garantir que todo o processo seja programático e reprodutível.

Automatizar a Inserção de Dados no DynamoDB: O script colocarArquivo.py que insere o nome do arquivo e a quantidade de linhas na tabela DynamoDB não está automatizado. Automatizar este processo para que ele seja executado automaticamente sempre que um novo arquivo for adicionado ao bucket S3.

### Observabilidade

A aplicação manda um email para uma determinada pessoa, quando ocorrer um push na branch main ou um pull request.
