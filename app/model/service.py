from flask import current_app as app
from flask_script import Command, Option

class StopService(Command):
    "Recalculate all workflow relationship paths"

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-s', '--service', dest='service', required=True),
        ] + self.client.options()

    def run(self, service, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            client.shutdown_service(service)

class StartService(Command):
    "Recalculate all workflow relationship paths"

    def __init__(self, client):
        self.client = client

    def get_options(self):
        return [
            Option('-s', '--service', dest='service', required=True),
        ] + self.client.options()

    def run(self, service, **kwargs):
        with app.app_context():
            client = self.client(**kwargs)
            client.startup_service(service)

