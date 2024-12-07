import boto3
import json
mysns = boto3.client('sns')

def lambda_handler(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    mysns.publish(
        TopicArn='arn:aws:sns:us-east-1:118421133023:topic-da-empresa-ada-de-contabilidade',
        Message=f'Arquivo de contabilidade colocado no bucket {bucket_name}: {object_key}',
        Subject=f'Bucket {bucket_name}'
    )


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

import io
import json
import logging
import zipfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LambdaWrapper:
    def __init__(self, lambda_client, iam_resource):
        self.lambda_client = lambda_client
        self.iam_resource = iam_resource

    def create_iam_role_for_lambda(self, iam_role_name):
        role = self.get_iam_role(iam_role_name)
        if role is not None:
            return role, False

        lambda_assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
        policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

        try:
            role = self.iam_resource.create_role(
                RoleName=iam_role_name,
                AssumeRolePolicyDocument=json.dumps(lambda_assume_role_policy),
            )
            logger.info("Created role %s.", role.name)
            role.attach_policy(PolicyArn=policy_arn)
            logger.info("Attached basic execution policy to role %s.", role.name)
        except ClientError as error:
            if error.response["Error"]["Code"] == "EntityAlreadyExists":
                role = self.iam_resource.Role(iam_role_name)
                logger.warning("The role %s already exists. Using it.", iam_role_name)
            else:
                logger.exception(
                    "Couldn't create role %s or attach policy %s.",
                    iam_role_name,
                    policy_arn,
                )
                raise

        return role, True

    def get_iam_role(self, iam_role_name):
        try:
            role = self.iam_resource.Role(iam_role_name)
            role.load()
            return role
        except ClientError:
            return None

    def create_function(self, function_name, handler_name, iam_role, deployment_package):
        try:
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Description="AWS Lambda doc example",
                Runtime="python3.9",
                Role=iam_role.arn,
                Handler=handler_name,
                Code={"ZipFile": deployment_package},
                Publish=True,
            )
            function_arn = response["FunctionArn"]
            waiter = self.lambda_client.get_waiter("function_active_v2")
            waiter.wait(FunctionName=function_name)
            logger.info(
                "Created function '%s' with ARN: '%s'.",
                function_name,
                response["FunctionArn"],
            )
        except ClientError:
            logger.error("Couldn't create function %s.", function_name)
            raise
        else:
            return function_arn

    def delete_function(self, function_name):
        try:
            self.lambda_client.delete_function(FunctionName=function_name)
        except ClientError:
            logger.exception("Couldn't delete function %s.", function_name)
            raise

def create_deployment_package(file_name, handler_name):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipped:
        zipped.write(file_name)
    buffer.seek(0)
    return buffer.read()

def main():
    # Inicializar a sessão Boto3 e os clientes
    sessao = boto3.Session(profile_name='default')
    lambda_client = sessao.client('lambda')
    iam_resource = sessao.resource('iam')

    # Inicializar o wrapper Lambda
    lambda_wrapper = LambdaWrapper(lambda_client, iam_resource)

    # Nome do papel IAM e da função Lambda
    iam_role_name = 'lambda-s3-role'
    function_name = 'lambda-ada-empresa-contabilidade'
    handler_name = 'lambdas3.lambda_handler'

    # Criar o papel IAM
    role, created = lambda_wrapper.create_iam_role_for_lambda(iam_role_name)
    if created:
        logger.info(f"Role '{iam_role_name}' foi criado com sucesso. ARN: {role.arn}")
    else:
        logger.info(f"Role '{iam_role_name}' já existia. Usando o ARN: {role.arn}")

    # Criar o pacote de implantação
    deployment_package = create_deployment_package('lambdas3.py', handler_name)

    # Criar a função Lambda
    function_arn = lambda_wrapper.create_function(function_name, handler_name, role, deployment_package)
    logger.info(f"Função Lambda criada com sucesso. ARN: {function_arn}")

    # Adicionar permissão para que o S3 invoque a função Lambda
    s3 = sessao.client('s3')
    sts = sessao.client('sts')
    idDaConta = sts.get_caller_identity()["Account"]
    bucket_name = 'bucket-da-empresa-ada-de-contabilidade-118421133023'

    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='S3InvokeLambdaPermission',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
        SourceAccount=idDaConta
    )

    # Configurar o evento de notificação do S3 para acionar a função Lambda
    s3.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': function_arn,
                    'Events': ['s3:ObjectCreated:*']
                }
            ]
        }
    )

if __name__ == "__main__":
    main()