from flask import Blueprint, request, jsonify # type: ignore
from app import db
from models import Categoria

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/categoria', methods=['POST'])
def criarCategoria():
    data = request.get_json()
    new_category = Categoria(nome=data['nome'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'id': new_category.id}), 201

@categoria_bp.route('/categoria/<int:categoria_id>', methods=['GET'])
def recuperarCategoria(categoria_id):
    category = Categoria.query.get_or_404(categoria_id)
    return jsonify({'id': category.id, 'nome': category.nome})

@categoria_bp.route('/categoria/<int:categoria_id>', methods=['PUT'])
def atualizarCategoria(categoria_id):
    data = request.get_json()
    category = Categoria.query.get_or_404(categoria_id)
    category.nome = data.get('nome', category.nome)
    db.session.commit()
    return jsonify({'id': category.id})

@categoria_bp.route('/categoria/<int:categoria_id>', methods=['DELETE'])
def deletarCategoria(categoria_id):
    category = Categoria.query.get_or_404(categoria_id)
    db.session.delete(category)
    db.session.commit()
    return '', 204
