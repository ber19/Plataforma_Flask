from flask import jsonify, request, Blueprint
from Plataforma.utils import ahora
from flask_login import login_required, current_user

urls_api = Blueprint('api', __name__)

@urls_api.route('/api/users', methods=["GET"])
@login_required
def get_users():
    if current_user.is_admin():
        from Plataforma.models import Usuarios
        users = [user.serialize() for user in Usuarios.query.all() ]
        return jsonify(users)
    else:
        return jsonify({"Error":"No es administrador"}), 401

@urls_api.route('/api/users/<id>', methods=["GET"])
@login_required
def get_user(id):
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no existe (GET)"}), 400
    if current_user.is_admin() or current_user.username == user.username:
        return jsonify(user.serialize())
    else:
        return jsonify({"Error":"No es admin o no es usted"}), 401

@urls_api.route('/api/users', methods=["POST"])
@login_required
def crear_user():
    if current_user.is_admin():
        from Plataforma.app import db
        json = request.get_json(force=True)
        if json.get('username') is None or json.get('contrasena') is None:
            return jsonify({'Error': 'Bad request'}), 400
        from Plataforma.models import Usuarios
        username = json.get('username')
        contrasena = json.get('contrasena')
        nombre = json.get('nombre')
        apellidos = json.get('apellidos')
        email = json.get('email')
        nuevo = Usuarios()
        nuevo.username = username
        nuevo.contrasena = contrasena
        nuevo.nombre = nombre
        nuevo.apellidos = apellidos
        nuevo.email = email
        nuevo.admin = False
        nuevo.creacion = ahora()
        nuevo.creado_por = current_user.username
        db.session.add(nuevo)
        db.session.commit()
        return jsonify(nuevo.serialize())
    else:
        return jsonify({"Error":"No es administrador"}), 401

@urls_api.route('/api/users/<id>', methods=['PUT'])
@login_required
def update_user(id):
    if current_user.is_admin():
        from Plataforma.app import db
        from Plataforma.models import Usuarios
        user = Usuarios.query.filter_by(id=id).first()
        if user is None:
            return jsonify({"Error": "El usuario no existe (PUT)"}), 400
        json = request.get_json(force=True)
        nombre = json.get('nombre')
        apellidos = json.get('apellidos')
        email = json.get('email')
        if nombre is None or nombre == "":
            return jsonify({"Error":"En el nombre"})
        else:
            user.nombre = nombre
        if apellidos is None or apellidos == "":
            return jsonify({"Error":"En el apellido"})
        else:
            user.apellidos = apellidos
        if email is None or email == "":
            return jsonify({"Error":"En el email"})
        else:
            user.email = email   
        db.session.commit()
        return jsonify(user.serialize())
    else:
        return jsonify({"Error": "No es administrador"}), 401

@urls_api.route('/api/users/<id>', methods=["DELETE"])
@login_required
def delete_user(id):
    if current_user.is_admin():
        from Plataforma.app import db
        from Plataforma.models import Usuarios
        user = Usuarios.query.filter_by(id=id).first()
        if user is None:
            return jsonify({"Error": "El usuario no existe (DELETE)"})
        deleted = user.serialize()
        db.session.delete(user)
        db.session.commit()
        return jsonify(deleted)
    else:
        return jsonify({"Error":"No es administrador"}), 401