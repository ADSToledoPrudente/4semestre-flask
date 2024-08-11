from flask import Flask # type: ignore
from models import db
from routes.anuncio_routes import anuncio_bp
from routes.categoria_routes import categoria_bp
from routes.compras_routes import compras_bp
from routes.favoritos_routes import favoritos_bp
from routes.perguntas_routes import perguntas_bp
from routes.relatorios_routes import relatorios_bp
from routes.respostas_routes import respostas_bp
from routes.usuario_routes import usuario_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(anuncio_bp, url_prefix='/api')
app.register_blueprint(categoria_bp, url_prefix='/api')
app.register_blueprint(compras_bp, url_prefix='/api')
app.register_blueprint(favoritos_bp, url_prefix='/api')
app.register_blueprint(perguntas_bp, url_prefix='/api')
app.register_blueprint(relatorios_bp, url_prefix='/api')
app.register_blueprint(respostas_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
