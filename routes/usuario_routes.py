from flask import Blueprint, request, jsonify # type: ignore
from app import db
from models import Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuario', methods=['POST'])
def criarUsuario():
    data = request.get_json()
    new_user = Usuario(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201

@usuario_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def recuperarUsuario(usuario_id):
    user = Usuario.query.get_or_404(usuario_id)
    return jsonify({
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'endereço': user.endereço,
        'telefone': user.telefone,
        'tipo': user.tipo
    }), 200

@usuario_bp.route('/usuario/<int:usuario_id>', methods=['PUT'])
def atualizarUsuario(usuario_id):
    data = request.get_json()
    user = Usuario.query.get_or_404(usuario_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({'id': user.id}), 200

@usuario_bp.route('/usuario/<int:usuario_id>', methods=['DELETE'])
def deletarUsuario(usuario_id):
    user = Usuario.query.get_or_404(usuario_id)
    db.session.delete(user)
    db.session.commit()
    return 'Usuário '+usuario_id+' deletado.', 204