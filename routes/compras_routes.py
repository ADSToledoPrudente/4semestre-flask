from flask import Blueprint, request, jsonify
from app import db
from models import Compras

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/compras', methods=['POST'])
def criarCompra():
    data = request.get_json()
    new_purchase = Compras(
        data_compra=data['data_compra'],
        quantidade=data['quantidade'],
        valor_total=data['valor_total'],
        comprador_id=data['comprador_id'],
        vendedor_id=data['vendedor_id'],
        anuncio_id=data['anuncio_id']
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({'id': new_purchase.id}), 201

@compras_bp.route('/compras/<int:compra_id>', methods=['GET'])
def recuperarCompra(compra_id):
    purchase = Compras.query.get_or_404(compra_id)
    return jsonify({
        'id': purchase.id,
        'data_compra': purchase.data_compra,
        'quantidade': purchase.quantidade,
        'valor_total': purchase.valor_total,
        'comprador_id': purchase.comprador_id,
        'vendedor_id': purchase.vendedor_id,
        'anuncio_id': purchase.anuncio_id
    })

@compras_bp.route('/compras/<int:compra_id>', methods=['PUT'])
def atualizarCompra(compra_id):
    data = request.get_json()
    purchase = Compras.query.get_or_404(compra_id)
    purchase.data_compra = data.get('data_compra', purchase.data_compra)
    purchase.quantidade = data.get('quantidade', purchase.quantidade)
    purchase.valor_total = data.get('valor_total', purchase.valor_total)
    db.session.commit()
    return jsonify({'id': purchase.id})

@compras_bp.route('/compras/<int:compra_id>', methods=['DELETE'])
def deletarCompra(compra_id):
    purchase = Compras.query.get_or_404(compra_id)
    db.session.delete(purchase)
    db.session.commit()
    return '', 204
