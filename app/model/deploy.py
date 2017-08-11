from flask import current_app as app
from flask_script import Command, Option
import time

class DeployService(Command):

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-task', '--task', dest='task', required=True),
            Option('-service', '--service', dest='service', required=True),
        ] + self.client.options()

    def run(self, task, service, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            task_definition = client.deploy_task(task)
            if service:
                client.deploy_service(service, task_definition)
                while not client.check_deployment(service, task_definition):
                    print('Waiting for %s to start on %s' % (task_definition, service))
                    time.sleep(30)
                print('%s started' % task_definition)




