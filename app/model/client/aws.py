import boto3
from flask_script import Option

class AwsClient():

    def __init__(self, key, secret, region):
        self.key = key
        self.secret = secret
        self.region = region

    @classmethod
    def options(cls):
        return [
            Option('-k', '--aws-key', dest='key', required=True),
            Option('-s', '--aws-secret', dest='secret', required=True),
            Option('-r', '--aws-region', dest='region', required=True),
        ]

    @property
    def client(self):
        return boto3.client(
            'ecs',
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region
        )

    def deploy_task(self, service_name, image, tag):
        existing_task = self.client.describe_task_definition(taskDefinition=service_name)
        existing_task['taskDefinition']['containerDefinitions'][0]['image'] = '%s:%s' % (image, tag)
        new_task = self.client.register_task_definition(family=service_name, containerDefinitions=existing_task['taskDefinition']['containerDefinitions'])
        return new_task['taskDefinition']['taskDefinitionArn']

    def deploy_service(self, cluster, service_name, task_definition):
        self.client.update_service(
            cluster=cluster,
            service=service_name,
            taskDefinition=task_definition
        )

    def check_deployment(self, cluster, service_name, new_task_definition):
        response = self.client.describe_services(cluster=cluster, services=[service_name, ])
        for deployment in response['services'][0]['deployments']:
            if deployment['taskDefinition'] == new_task_definition and deployment['desiredCount'] == deployment['runningCount']:
                return True
        return False

    def shutdown_service(self, cluster, service_name):
        self.client.update_service(
            cluster=cluster,
            service=service_name,
            desiredCount=0
        )

    def startup_service(self, cluster, service_name):
        self.client.update_service(
            cluster=cluster,
            service=service_name,
            desiredCount=1
        )

    def task_status(self, id):
        response = self.client.describe_tasks(cluster='default', tasks=[id])
        return response.get('tasks')[0].get('lastStatus', 'STOPPED')

    def start_task(self, cluster, definition, cargs):
        response = self.client.run_task(
            cluster=cluster,
            taskDefinition=definition,
            overrides=dict(
                containerOverrides=[
                    dict(
                        name='main',
                        command=cargs
                    )
                ]
            )
        )

        return response.get('tasks')[0].get('taskArn', None)