from flask import Flask
from config import Config
from models.database import init_db

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
init_db()

# Importar controladores después de crear app para evitar importaciones circulares
from controllers import auth_controller, task_controller

# Registrar blueprints
app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(task_controller.task_bp)

if __name__ == '__main__':
    app.run(debug=True)