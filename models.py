import datetime
from app import db

class Usuario(db.Model):
    def __init__(self, nome, email, senha, endereco, telefone, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco
        self.telefone = telefone
        self.tipo = tipo
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    tipo = db.Column(db.Integer)  # 1 - comprador ou 2 - vendedor

class Anuncio(db.Model):
    def __init__(self, titulo, descricao, preco, categoria_id, status=1):
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.data_criacao = datetime.datetime.now()  # Define a data de criação automaticamente
        self.status = status
        self.categoria_id = categoria_id
        
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('anuncios', lazy=True))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Perguntas(db.Model):
    __tablename__ = 'perguntas'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    anuncio_id = db.Column(db.Integer, nullable=False)
    respostas = db.relationship('Respostas', backref='pergunta', lazy=True)
    usuario = db.relationship('Usuario', backref='perguntas', lazy=True)

class Respostas(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('perguntas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='respostas', lazy=True)

class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    comprador_id = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, nullable=False)
    anuncio_id = db.Column(db.Integer, nullable=False)

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_adicionado = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    anuncio_id = db.Column(db.Integer, nullable=False)

class RelatorioVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_vendas = db.Column(db.Float)
    total_receita = db.Column(db.Float)
    vendedor_id = db.Column(db.Integer, nullable=False)

class RelatorioCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_compras = db.Column(db.Integer)
    total_gasto = db.Column(db.Float)
    comprador_id = db.Column(db.Integer, nullable=False)
