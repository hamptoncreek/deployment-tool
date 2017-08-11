from flask import Flask
from flask_script import Manager

from app.models

app = Flask(__name__)

manager = Manager(app)
manager.add_command('start-and-wait', task.StartAndWait())

if __name__ == '__main__':
    manager.run()