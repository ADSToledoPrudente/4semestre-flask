from flask import Blueprint, redirect, render_template, request, jsonify, url_for # type: ignore
from app import db, login_required, current_user
from models import Anuncio, Categoria, Perguntas

anuncio_bp = Blueprint('anuncio', __name__)

@anuncio_bp.route('/anuncio', methods=['POST'])
def criarAnuncio():
    data = request.get_json()
    new_ad = Anuncio(**data)
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({'id': new_ad.id}), 201

@anuncio_bp.route('/anuncio/<int:anuncio_id>', methods=['GET'])
def recuperarAnuncio(anuncio_id):
    ad = Anuncio.query.get_or_404(anuncio_id)
    return jsonify({
        'id': ad.id,
        'titulo': ad.titulo,
        'descricao': ad.descricao,
        'preco': ad.preco,
        'data_criacao': ad.data_criacao,
        'status': ad.status,
        'usuario_id': ad.usuario_id,
        'categoria_id': ad.categoria_id
    }), 200

@anuncio_bp.route('/anuncio/<int:anuncio_id>', methods=['PUT'])
def atualizarAnuncio(anuncio_id):
    data = request.get_json()
    ad = Anuncio.query.get_or_404(anuncio_id)
    for key, value in data.items():
        setattr(ad, key, value)
    db.session.commit()
    return jsonify({'id': ad.id}), 200

@anuncio_bp.route('/anuncio/<int:anuncio_id>', methods=['DELETE'])
def deletarAnuncio(anuncio_id):
    ad = Anuncio.query.get_or_404(anuncio_id)
    db.session.delete(ad)
    db.session.commit()
    return '', 204

@anuncio_bp.route("/anuncios")
def anuncios():
    return render_template('anuncios/anuncios.html')

@anuncio_bp.route("/todosanuncios")
def recuperarTodos():
    anuncios = Anuncio.query.all()
    anuncios_dict = [
        {
            'id': anuncio.id,
            'titulo': anuncio.titulo,
            'descricao': anuncio.descricao,
            'preco': anuncio.preco,
            'status': anuncio.status,
            'categoria': anuncio.categoria.nome,
            'categoriaId': anuncio.categoria.id
        } for anuncio in anuncios
    ]
    
    return jsonify(anuncios_dict)
    
@anuncio_bp.route('/gerenciarAnuncio', defaults={'anuncioId': None}, methods=['GET', 'POST'])
@anuncio_bp.route('/gerenciarAnuncio/<int:anuncioId>', methods=['GET', 'POST', 'PUT'])
@login_required
def gerenciarAnuncio(anuncioId):
    if request.method == 'POST':
        
        if request.form.get('_method') == 'PUT' and anuncioId:
            anuncio = Anuncio.query.get_or_404(anuncioId)
            
            anuncio.titulo = request.form['titulo']
            anuncio.descricao = request.form['descricao']
            anuncio.preco = request.form['preco']
            anuncio.categoriaId = request.form['categoriaId']
            
            for key, value in request.form.items():
                setattr(anuncio, key, value)
            db.session.commit()
            return redirect(url_for('anuncios.anuncios'))
        
        else:
            
            novoAnuncio = Anuncio(
                titulo = request.form['titulo'],
                descricao = request.form['descricao'],
                preco = request.form['preco'],
                categoria_id = request.form['categoriaId'],
            )
            
            db.session.add(novoAnuncio)
            db.session.commit()
            return redirect(url_for('anuncios.anuncios'))
        
    categorias = Categoria.query.all()
    if anuncioId:
        anuncio = Anuncio.query.get_or_404(anuncioId)
        return render_template('anuncios/gerenciar_anuncio.html', anuncio=anuncio, categorias=categorias, edit=True)
    else:
        print('aqui 4')
        return render_template('anuncios/gerenciar_anuncio.html', anuncio=None, categorias=categorias, edit=False)
    
@anuncio_bp.route('/visualizarAnuncio/<int:anuncioId>', methods=['GET', 'POST', 'PUT'])
def visualizarAnuncio(anuncioId):
    categorias = Categoria.query.all()
    anuncio = Anuncio.query.get_or_404(anuncioId)
    perguntas = Perguntas.query.filter_by(anuncio_id = anuncioId).order_by(Perguntas.data_criacao.desc())
    return render_template('anuncios/visualizar_anuncio.html', anuncio=anuncio, usuario=current_user, perguntas=perguntas, categorias=categorias, edit=True)