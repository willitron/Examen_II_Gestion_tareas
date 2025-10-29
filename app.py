from flask import Flask
from config import Config
from models.database import init_db

app = Flask(__name__)
app.config.from_object(Config)

init_db()

from controllers import auth_controller, task_controller

app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(task_controller.task_bp)

if __name__ == '__main__':
    app.run(debug=True)