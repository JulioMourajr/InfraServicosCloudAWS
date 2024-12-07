import boto3

sessao = boto3.Session(profile_name='default')

qtd_linhas = 0

s3 = sessao.client('s3')
dynamodb = sessao.client('dynamodb')

lista = s3.list_buckets()

for bucket in lista['Buckets']:
    meubucket=bucket['Name']

print(meubucket)

arquivos = s3.list_objects(Bucket=meubucket)

if 'Contents' in arquivos:
    for arquivo in arquivos['Contents']:
        nomeArquivo = arquivo['Key']
        print(f"Nome do arquivo: {nomeArquivo}")

        meus3 = s3.get_object(Bucket=meubucket, Key=nomeArquivo)

        conteudo = meus3['Body'].read().decode('utf-8')

        qtd_linhas = len(conteudo.split('\n'))

        try:

            dynamodb.put_item(
                TableName='tabela-da-empresa-ada-de-contabilidade',
                Item={
                    'nome_do_arquivo': {'S': nomeArquivo},
                    'quantidade_de_Linhas': {'N': str(qtd_linhas)}
                }
            )
            print("Arquivo inserido com sucesso!")
        except Exception as e:
            print("Erro ao inserir arquivo:", e)
else:
    print("Nenhum arquivo encontrado no bucket")

print("Concluído!")