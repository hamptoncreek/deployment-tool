import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cluster', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--secret', required=True)
parser.add_argument('--region', required=True)
parser.add_argument('--service', required=True)
parser.add_argument('--status', required=True)

args = parser.parse_args()

client = boto3.client(
    'ecs',
    aws_access_key_id=args.key,
    aws_secret_access_key=args.secret,
    region_name=args.region
)

def shutdown_service(service_name):
    client.update_service(
        cluster=args.cluster,
        service=service_name,
        desiredCount=0
    )

def startup_service(service_name):
    client.update_service(
        cluster=args.cluster,
        service=service_name,
        desiredCount=1
    )

if args.status == 'stop':
    shutdown_service(args.service)
    print('%s stopped' % args.service)
else:
    startup_service(args.service)
    print('%s started' % args.service)

