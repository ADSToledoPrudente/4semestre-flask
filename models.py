from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    endereço = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    tipo = db.Column(db.Integer)  # 1 - comprador ou 2 - vendedor
    anuncios = db.relationship('Anuncio', backref='usuario', lazy=True)
    perguntas = db.relationship('Perguntas', backref='usuario', lazy=True)
    respostas = db.relationship('Respostas', backref='usuario', lazy=True)
    compras = db.relationship('Compras', backref='comprador', lazy=True)
    vendas = db.relationship('Compras', backref='vendedor', lazy=True)
    favoritos = db.relationship('Favoritos', backref='usuario', lazy=True)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    título = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('Categoria.id'), nullable=False)
    perguntas = db.relationship('Perguntas', backref='anuncio', lazy=True)
    compras = db.relationship('Compras', backref='anuncio', lazy=True)
    favoritos = db.relationship('Favoritos', backref='anuncio', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    anuncios = db.relationship('Anuncio', backref='categoria', lazy=True)

class Perguntas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('Anuncio.id'), nullable=False)
    respostas = db.relationship('Respostas', backref='pergunta', lazy=True)

class Respostas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('Perguntas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)

class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('Anuncio.id'), nullable=False)

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_adicionado = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('Anuncio.id'), nullable=False)

class RelatorioVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_vendas = db.Column(db.Float)
    total_receita = db.Column(db.Float)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)

class RelatorioCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_compras = db.Column(db.Integer)
    total_gasto = db.Column(db.Float)
    comprador_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
