import boto3
sessao = boto3.Session(profile_name='default')

dynamodb = sessao.client('dynamodb')

criarTabela = dynamodb.create_table(
    TableName='tabela-da-empresa-ada-de-contabilidade',
    KeySchema=[
        {
            'AttributeName': 'nome_do_arquivo',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'quantidade_de_Linhas',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'nome_do_arquivo',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'quantidade_de_Linhas',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("A tabela foi criada com sucesso!")
