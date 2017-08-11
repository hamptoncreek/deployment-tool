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
        ] + self.client.get_options()

    def task_status(client, id):
        response = client.describe_tasks(cluster='default', tasks=[id])
        return response.get('tasks')[0].get('lastStatus', 'STOPPED')

    def start_task(client, definition, cargs):
        response = client.run_task(
            cluster=args.cluster,
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

    def run(self, definition, command):
        with app.app_context():
            print('test')
            # task_id = self.start_task(definition, command)
            # print('%s started' % definition)
            # status = 'PENDING'
            # while status in ['PENDING', 'RUNNING']:
            #     status = self.task_status(task_id)
            #     time.sleep(30)
            #     print('Waiting for %s to stop, currently %s' % (task_id, status))

