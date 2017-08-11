import argparse
import time

import boto3

parser = argparse.ArgumentParser()
parser.add_argument('--cluster', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--secret', required=True)
parser.add_argument('--region', required=True)
parser.add_argument('--task', required=True)
parser.add_argument('--tag', required=True)
parser.add_argument('--image', required=True)
parser.add_argument('--service')

args = parser.parse_args()

client = boto3.client(
    'ecs',
    aws_access_key_id=args.key,
    aws_secret_access_key=args.secret,
    region_name=args.region
)

def deploy_task(service_name):
    existing_task = client.describe_task_definition(taskDefinition=service_name)
    existing_task['taskDefinition']['containerDefinitions'][0]['image'] = '%s:%s' % (args.image, args.tag)
    new_task = client.register_task_definition(family=service_name, containerDefinitions=existing_task['taskDefinition']['containerDefinitions'])
    return new_task['taskDefinition']['taskDefinitionArn']

def deploy_service(service_name, task_definition):
    client.update_service(
        cluster=args.cluster,
        service=service_name,
        taskDefinition=task_definition
    )

def check_deployment(service_name, new_task_definition):
    response = client.describe_services(cluster=args.cluster,services=[service_name,])
    for deployment in response['services'][0]['deployments']:
        if deployment['taskDefinition'] == new_task_definition and deployment['desiredCount'] == deployment['runningCount']:
            return True
    return False

task_definition = deploy_task(args.task)
if args.service:
    deploy_service(args.service, task_definition)
    while not check_deployment(args.service, task_definition):
        print('Waiting for %s to start on %s' % (task_definition, args.service))
        time.sleep(30)
    print('%s started' % task_definition)

