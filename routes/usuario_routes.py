from flask import Blueprint, redirect, render_template, request, jsonify, url_for # type: ignore
from app import db, login_user, login_required, logout_user, login_manager
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
    return jsonify({ 'sucesso': user.id }), 200

@usuario_bp.route("/usuarios")
def usuarios():
    return render_template('usuario/usuario.html')

@usuario_bp.route("/todosusuarios")
def recuperarTodos():
    usuarios = Usuario.query.all()
    usuarios_dict = [
        {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email
        } for usuario in usuarios
    ]
    
    return jsonify(usuarios_dict)
    
@usuario_bp.route('/gerenciarUsuario', defaults={'usuarioId': None}, methods=['GET', 'POST'])
@usuario_bp.route('/gerenciarUsuario/<int:usuarioId>', methods=['GET', 'POST', 'PUT'])
@login_required
def gerenciarUsuario(usuarioId):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT' and usuarioId:
            usuario = Usuario.query.get_or_404(usuarioId)
            
            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.senha = request.form['senha']
            usuario.endereco = request.form['endereco']
            usuario.telefone = request.form['telefone']
            usuario.tipo = request.form['tipo']
            
            for key, value in request.form.items():
                setattr(usuario, key, value)
            db.session.commit()
            return redirect(url_for('usuario.usuarios'))
        
        else:
            novoUsuario = Usuario(
                nome = request.form['nome'],
                email = request.form['email'],
                senha = request.form['senha'],
                endereco = request.form['endereco'],
                telefone = request.form['telefone'],
                tipo = request.form['tipo']
            )
            
            db.session.add(novoUsuario)
            db.session.commit()
            return redirect(url_for('usuario.usuarios'))
        
    if usuarioId:
        usuario = Usuario.query.get_or_404(usuarioId)
        return render_template('usuario/gerenciar_usuario.html', usuario=usuario, edit=True)
    else:
        return render_template('usuario/gerenciar_usuario.html', usuario=None, edit=False)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Usuario.query.filter_by(email=email, senha=password).first()
        
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html')

@usuario_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('usuario.login'))

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)