from flask import Flask
from flask_script import Manager

from app.model import task, deploy, service
from app.model.client.aws import AwsClient

app = Flask(__name__)

manager = Manager(app)
manager.add_command('start-task-and-wait', task.StartAndWait(AwsClient))
manager.add_command('start-service', service.StartService(AwsClient))
manager.add_command('stop-service', service.StopService(AwsClient))
manager.add_command('deploy-service', deploy.DeployService(AwsClient))

if __name__ == '__main__':
    manager.run()