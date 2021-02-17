from flask import jsonify, request, Blueprint
from Plataforma.utils import ahora
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

api_actividad = Blueprint('api_actividad', __name__)

@api_actividad.route('/api/actividad', methods=["GET"])
@login_required
def get_actividades():
    if current_user.is_admin():
        from Plataforma.models import Actividad
        actividades = [activ.serialize() for activ in Actividad.query.all()]
        return jsonify(actividades)
    else:
        return jsonify({"Error":"No es administrador"}), 401 

@api_actividad.route('/api/actividad/<id>', methods=["GET"])
@login_required
def get_actividades_user(id):
    if current_user.is_admin() or current_user.id==int(id):
        from Plataforma.models import Actividad
        actividades = [activ.serialize() for activ in Actividad.query.filter_by(user_id=id)]
        if len(actividades) == 0:
            return jsonify({"Error": "No hay actividades (GET)"}), 400
        return jsonify(actividades)
    else:
        return jsonify({"Error":"No es administrador o no es usted"})

@api_actividad.route('/api/actividad', methods=["POST"])
@login_required
def crear_actividad():
    if not current_user.is_admin():
        from Plataforma.app import db, app
        from Plataforma.models import Actividad
        json = request.get_json(force=True)
        activ = json.get('activ')
        comentarios = json.get('comentarios')
        creacion = ahora()
        archivo = json.get('archivo')
        ar = open(f"{archivo}", "rb")
        datos = ar.read()
        nombre = f"{activ}_{ahora()}.rar"
        nombre_archiv = secure_filename(nombre)
        f = open(f"{app.config['UPLOAD_FOLDER']}/{nombre_archiv}", "xb")
        f.write(datos)
        nueva = Actividad()
        nueva.user_id = current_user.id
        nueva.activ = activ
        nueva.comentarios = comentarios
        nueva.archivo = nombre_archiv
        nueva.creacion = creacion
        db.session.add(nueva)
        db.session.commit()
        return jsonify(nueva.serialize())
    else:
        return jsonify({"Error":"Es administrador"}), 401

