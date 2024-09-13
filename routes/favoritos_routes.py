from flask import Blueprint, request, jsonify
from app import db
from models import Favoritos

favoritos_bp = Blueprint('favoritos', __name__)

@favoritos_bp.route('/favoritos', methods=['POST'])
def criarFavorito():
    data = request.get_json()
    new_favorite = Favoritos(
        data_adicionado=data['data_adicionado'],
        usuario_id=data['usuario_id'],
        anuncio_id=data['anuncio_id']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'id': new_favorite.id}), 201

@favoritos_bp.route('/favoritos/<int:favorito_id>', methods=['GET'])
def recuperarFavorito(favorito_id):
    favorite = Favoritos.query.get_or_404(favorito_id)
    return jsonify({
        'id': favorite.id,
        'data_adicionado': favorite.data_adicionado,
        'usuario_id': favorite.usuario_id,
        'anuncio_id': favorite.anuncio_id
    })

@favoritos_bp.route('/favoritos/<int:favorito_id>', methods=['PUT'])
def atualizarFavorito(favorito_id):
    data = request.get_json()
    favorite = Favoritos.query.get_or_404(favorito_id)
    favorite.data_adicionado = data.get('data_adicionado', favorite.data_adicionado)
    db.session.commit()
    return jsonify({'id': favorite.id})

@favoritos_bp.route('/favoritos/<int:favorito_id>', methods=['DELETE'])
def deletarFavorito(favorito_id):
    favorite = Favoritos.query.get_or_404(favorito_id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204
