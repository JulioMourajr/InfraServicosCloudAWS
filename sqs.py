import boto3
import json

sessao = boto3.Session(profile_name='default')

client_sqs = sessao.client('sqs')

response = client_sqs.create_queue(
    QueueName='fila-da-empresa-ada-de-contabilidade',
)

urldafila = response['QueueUrl']
arndafila = client_sqs.get_queue_attributes(
    QueueUrl=urldafila,
    AttributeNames=['QueueArn']
)['Attributes']['QueueArn']

mysns = sessao.client('sns')

meusTopicos = mysns.list_topics()

topicoArn = meusTopicos['Topics'][0]['TopicArn']

mysns.subscribe(
    TopicArn=topicoArn,
    Protocol='sqs',
    Endpoint=arndafila,
)

print("A fila foi criada com sucesso! URL:", response['QueueUrl'])
print("Assinatura criada com sucesso. ARN da Fila:", arndafila)
print("Topico criado com sucesso. ARN do Tópico:", topicoArn)