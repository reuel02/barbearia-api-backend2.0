from src.routes.auth_routes import auth_bp
from flask import Flask
from db import db
from flask_migrate import Migrate
from src.routes.agendamentos_routes import agendamentos_bp
from src.routes.servicos_routes import servicos_bp
from src.routes.usuarios_routes import usuarios_bp
import src.models
from flask_jwt_extended import JWTManager
import os

# Instancia do Flask
app = Flask(__name__)

# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost:8081/barbearia_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configura JWT com uma chave secreta importada do .env
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "minha-chave-secreta-teste")

# Conecta o banco de dados à aplicação
db.init_app(app)

# Instancia e conecta o alembic
migrate = Migrate(app, db)

# Inicializa o JWT
jwt = JWTManager(app)

# Registra o Blueprint das rotas, atribuindo um prefixo
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(agendamentos_bp, url_prefix="/api/agendamentos")
app.register_blueprint(servicos_bp, url_prefix="/api/servicos")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")

# Permite o servidor rodar sem parar
if __name__ == "__main__":

    app.run(debug=True)
