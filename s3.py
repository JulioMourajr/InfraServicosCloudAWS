import boto3

sessao = boto3.Session(profile_name='default')

client_s3 = sessao.client('s3')

response = client_s3.create_bucket(
    Bucket='bucket-da-empresa-ada-de-contabilidade-118421133023',
)

print("O bucket foi criado com sucesso!")