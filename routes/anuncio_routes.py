from flask import Blueprint, request, jsonify # type: ignore
from app import db
from models import Anuncio

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
        'título': ad.título,
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
