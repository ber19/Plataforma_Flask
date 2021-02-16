from flask import jsonify, request, Blueprint
from Plataforma.utils import ahora
from werkzeug.utils import secure_filename

api_actividad = Blueprint('api_actividad', __name__)

@api_actividad.route('/api/actividad', methods=["GET"])
def get_actividades():
    from Plataforma.models import Actividad
    actividades = [activ.serialize() for activ in Actividad.query.all()]
    return jsonify(actividades)

@api_actividad.route('/api/actividad/<id>', methods=["GET"])
def get_actividades_user(id):
    from Plataforma.models import Actividad
    actividades = [activ.serialize() for activ in Actividad.query.filter_by(user_id=id)]
    if len(actividades) == 0:
        return jsonify({"Error": "No hay actividades (GET)"}), 400
    return jsonify(actividades)

@api_actividad.route('/api/actividad', methods=["POST"])
def crear_actividad():
    from Plataforma.models import Usuarios
    json = request.get_json(force=True)
    user_id = json.get('user_id')
    user = Usuarios.query.filter_by(id=user_id).first()
    if user_id is None or user_id == "":
        return jsonify({"Error": "No hay user_id"}), 400
    elif user is None or user.is_admin() == True:
        return jsonify({"Error": "El usuario es admin o no existe"}), 400
    else:
        from Plataforma.app import db, app
        from Plataforma.models import Actividad
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
        nueva.user_id = user_id
        nueva.activ = activ
        nueva.comentarios = comentarios
        nueva.archivo = nombre_archiv
        nueva.creacion = creacion
        db.session.add(nueva)
        db.session.commit()
        return jsonify(nueva.serialize())

