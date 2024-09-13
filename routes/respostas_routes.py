import datetime
from flask import Blueprint, redirect, request, jsonify, url_for
from flask_login import current_user, login_required
from app import db
from models import Respostas

respostas_bp = Blueprint('respostas', __name__)

@respostas_bp.route('/respostas', methods=['POST'])
def criarResposta():
    data = request.get_json()
    new_answer = Respostas(
        conteudo=data['conteudo'],
        data_criacao=data['data_criacao'],
        pergunta_id=data['pergunta_id'],
        usuario_id=data['usuario_id']
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({'id': new_answer.id}), 201

@respostas_bp.route('/respostas/<int:resposta_id>', methods=['GET'])
def recuperarResposta(resposta_id):
    answer = Respostas.query.get_or_404(resposta_id)
    return jsonify({
        'id': answer.id,
        'conteudo': answer.conteudo,
        'data_criacao': answer.data_criacao,
        'pergunta_id': answer.pergunta_id,
        'usuario_id': answer.usuario_id
    })

@respostas_bp.route('/respostas/<int:resposta_id>', methods=['PUT'])
def atualizarResposta(resposta_id):
    data = request.get_json()
    answer = Respostas.query.get_or_404(resposta_id)
    answer.conteudo = data.get('conteudo', answer.conteudo)
    answer.data_criacao = data.get('data_criacao', answer.data_criacao)
    db.session.commit()
    return jsonify({'id': answer.id})

@respostas_bp.route('/respostas/<int:resposta_id>', methods=['DELETE'])
def deletarUsuario(resposta_id):
    answer = Respostas.query.get_or_404(resposta_id)
    db.session.delete(answer)
    db.session.commit()
    return '', 204

@respostas_bp.route('/novaResposta', methods=['POST'])
@login_required
def novaResposta():
    conteudo = request.form['conteudo']
    perguntaId = request.form['perguntaId']
    usuario_id = current_user.id
    
    nova_resposta = Respostas(conteudo=conteudo, data_criacao=datetime.datetime.now(), pergunta_id=perguntaId, usuario_id=usuario_id)
    
    db.session.add(nova_resposta)
    db.session.commit()
    
    return redirect(url_for('anuncio.visualizarAnuncio', anuncioId=nova_resposta.pergunta.anuncio_id))