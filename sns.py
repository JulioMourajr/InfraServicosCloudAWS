import boto3
import json

sessao = boto3.Session(profile_name='default')

client_sns = sessao.client('sns')

response = client_sns.create_topic(
    Name='topic-da-empresa-ada-de-contabilidade',
)

topicoCriado = response['TopicArn']

assinatura = client_sns.subscribe(
    TopicArn=topicoCriado,
    Protocol='email',
    Endpoint='juliomourajr@hotmail.com',
)

with open('sns_topic_arn.json', 'w') as f:
    json.dump({'TopicArn': topicoCriado}, f)

print("O tópico foi criado com sucesso! ARN:", response['TopicArn'])
print("Assinatura criada com sucesso. ARN da Assinatura:", assinatura)