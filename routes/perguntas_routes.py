from flask import Blueprint, request, jsonify # type: ignore
from app import db
from models import Perguntas

perguntas_bp = Blueprint('perguntas', __name__)

@perguntas_bp.route('/perguntas', methods=['POST'])
def criarPergunta():
    data = request.get_json()
    new_question = Perguntas(
        conteudo=data['conteudo'],
        data_criacao=data['data_criacao'],
        usuario_id=data['usuario_id'],
        anuncio_id=data['anuncio_id']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'id': new_question.id}), 201

@perguntas_bp.route('/perguntas/<int:pergunta_id>', methods=['GET'])
def recuperarPergunta(pergunta_id):
    question = Perguntas.query.get_or_404(pergunta_id)
    return jsonify({
        'id': question.id,
        'conteudo': question.conteudo,
        'data_criacao': question.data_criacao,
        'usuario_id': question.usuario_id,
        'anuncio_id': question.anuncio_id
    })

@perguntas_bp.route('/perguntas/<int:pergunta_id>', methods=['PUT'])
def atualizarPergunta(pergunta_id):
    data = request.get_json()
    question = Perguntas.query.get_or_404(pergunta_id)
    question.conteudo = data.get('conteudo', question.conteudo)
    question.data_criação = data.get('data_criacao', question.data_criação)
    db.session.commit()
    return jsonify({'id': question.id})

@perguntas_bp.route('/perguntas/<int:pergunta_id>', methods=['DELETE'])
def deletarPergunta(pergunta_id):
    question = Perguntas.query.get_or_404(pergunta_id)
    db.session.delete(question)
    db.session.commit()
    return '', 204
