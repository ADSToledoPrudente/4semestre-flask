from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, login_manager
from flask import Blueprint, redirect, render_template, request, jsonify, url_for # type: ignore

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://4_flaskuser:qwe123@bd.iron.hostazul.com.br:4406/4_flaskdb'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'chave super hiper secreta'
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

from routes.usuario_routes import usuario_bp
from routes.anuncio_routes import anuncio_bp
from routes.categoria_routes import categoria_bp
from routes.compras_routes import compras_bp
from routes.favoritos_routes import favoritos_bp
from routes.perguntas_routes import perguntas_bp
from routes.relatorios_routes import relatorios_bp
from routes.respostas_routes import respostas_bp

app.register_blueprint(anuncio_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(favoritos_bp)
app.register_blueprint(perguntas_bp)
app.register_blueprint(relatorios_bp)
app.register_blueprint(respostas_bp)
app.register_blueprint(usuario_bp)

@app.route("/")
def index():
    return render_template('index.html')

@app.cli.command('create-tables')
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)