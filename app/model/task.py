import time

from flask import current_app as app
from flask_script import Command, Option

class StartAndWait(Command):
    "Recalculate all workflow relationship paths"

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-d', '--definition', dest='definition', required=True),
            Option('-c', '--command', dest='command', required=True),
        ] + self.client.options()

    def run(self, definition, command, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            task_id = client.start_task(definition, command)
            print('%s started' % definition)
            status = 'PENDING'
            while status in ['PENDING', 'RUNNING']:
                status = client.task_status(task_id)
                time.sleep(30)
                print('Waiting for %s to stop, currently %s' % (task_id, status))

