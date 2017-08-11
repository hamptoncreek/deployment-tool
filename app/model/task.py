import time

from flask import current_app as app
from flask_script import Command, Option

class StartAndWait(Command):
    "Recalculate all workflow relationship paths"

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-cluster', '--cluster', dest='cluster', required=True),
            Option('-definition', '--definition', dest='definition', required=True),
            Option('-command', '--command', dest='command', required=True),
        ] + self.client.options()

    def run(self, cluster, definition, command, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            task_id = client.start_task(cluster, definition, command)
            print('%s started' % definition)
            status = 'PENDING'
            while status in ['PENDING', 'RUNNING']:
                status = client.task_status(task_id)
                time.sleep(30)
                print('Waiting for %s to stop, currently %s' % (task_id, status))

class StartMultipleAndWait(Command):
    "Recalculate all workflow relationship paths"

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-cluster', '--cluster', dest='cluster', required=True),
            Option('-definition', '--definition', dest='definition', required=True),
            Option('-command', '--command', dest='command', required=True),
            Option('-page', '--page', dest='page', required=True),
        ] + self.client.options()

    def run(self, cluster, definition, command, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            command
            task_id = client.start_task(cluster, definition, command)
            print('%s started' % definition)
            status = 'PENDING'
            while status in ['PENDING', 'RUNNING']:
                status = client.task_status(task_id)
                time.sleep(30)
                print('Waiting for %s to stop, currently %s' % (task_id, status))


