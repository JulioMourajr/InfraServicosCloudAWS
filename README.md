
# AWS Resource Management

Este projeto cria e gerencia recursos da AWS, incluindo buckets S3, tópicos SNS e filas SQS.

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

## Observações

- O arquivo `sns_topic_arn.json` é ignorado pelo Git devido ao `.gitignore` e é usado para armazenar o ARN do tópico SNS criado.
- Certifique-se de que suas credenciais AWS estão configuradas corretamente para que os scripts possam acessar os serviços AWS.

