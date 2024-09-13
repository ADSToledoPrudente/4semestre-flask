from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from app import db
from models import Anuncio, Categoria, Favoritos, Perguntas

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
    from flask_login import current_user

    anuncios = Anuncio.query.all()
    anuncios_favoritados = []
    anuncios_nao_favoritados = []

    for anuncio in anuncios:
        if current_user.is_authenticated:
            favoritado = Favoritos.query.filter_by(usuario_id=current_user.id, anuncio_id=anuncio.id).first() is not None
        else:
            favoritado = False
        
        anuncio_dict = {
            'id': anuncio.id,
            'titulo': anuncio.titulo,
            'preco': anuncio.preco,
            'categoria': anuncio.categoria.nome,
            'favoritado': favoritado
        }

        if favoritado:
            anuncios_favoritados.append(anuncio_dict)
        else:
            anuncios_nao_favoritados.append(anuncio_dict)

    anuncios_com_favoritos = anuncios_favoritados + anuncios_nao_favoritados
    
    return jsonify(anuncios_com_favoritos)

from flask_login import login_required
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
                titulo=request.form['titulo'],
                descricao=request.form['descricao'],
                preco=request.form['preco'],
                categoria_id=request.form['categoriaId'],
            )
            
            db.session.add(novoAnuncio)
            db.session.commit()
            return redirect(url_for('anuncios.anuncios'))
        
    categorias = Categoria.query.all()
    if anuncioId:
        anuncio = Anuncio.query.get_or_404(anuncioId)
        return render_template('anuncios/gerenciar_anuncio.html', anuncio=anuncio, categorias=categorias, edit=True)
    else:
        return render_template('anuncios/gerenciar_anuncio.html', anuncio=None, categorias=categorias, edit=False)

@anuncio_bp.route('/visualizarAnuncio/<int:anuncioId>', methods=['GET', 'POST', 'PUT'])
def visualizarAnuncio(anuncioId):
    from flask_login import current_user

    categorias = Categoria.query.all()
    anuncio = Anuncio.query.get_or_404(anuncioId)
    perguntas = Perguntas.query.filter_by(anuncio_id=anuncioId).order_by(Perguntas.data_criacao.desc())
    return render_template('anuncios/visualizar_anuncio.html', anuncio=anuncio, usuario=current_user, perguntas=perguntas, categorias=categorias, edit=True)