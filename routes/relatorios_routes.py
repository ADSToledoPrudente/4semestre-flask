from flask import Blueprint, jsonify
from models import RelatorioCompra, RelatorioVenda

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorioVenda', methods=['GET'])
def getRelatorioVenda():
    reports = RelatorioVenda.query.all()
    return jsonify([{
        'id': report.id,
        'total_vendas': report.total_vendas,
        'total_receita': report.total_receita,
        'vendedor_id': report.vendedor_id
    } for report in reports])

@relatorios_bp.route('/relatorioCompra', methods=['GET'])
def getRelatorioCompra():
    reports = RelatorioCompra.query.all()
    return jsonify([{
        'id': report.id,
        'total_compras': report.total_compras,
        'total_gasto': report.total_gasto,
        'comprador_id': report.comprador_id
    } for report in reports])
