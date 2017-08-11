import boto3
from flask_script import Option

class AwsClient():
    def get_options(self):
        return [
            Option('-k', '--aws-key', dest='key'),
            Option('-s', '--aws-secret', dest='secret'),
            Option('-r', '--aws-region', dest='region'),
        ]

    def client(self, key, secret, region):
        return boto3.client(
            'ecs',
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            region_name=region
        )