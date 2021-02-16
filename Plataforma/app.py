from re import I
from flask import Flask, render_template, redirect, \
    abort, send_from_directory, jsonify, request
from Plataforma import config
from Plataforma.forms import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, \
    login_required, current_user
from Plataforma.utils import ahora


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    from Plataforma.models import Usuarios
    return Usuarios.query.get(int(user_id))

#---------------------------------------------------------------------------------
@app.route("/", methods=["get", "post"])
def login():
    from Plataforma.models import Usuarios
    if current_user.is_authenticated and current_user.is_admin():
        return redirect("/admin")
    elif current_user.is_authenticated and not current_user.is_admin():
        return redirect("/usuario")
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = Usuarios.query.filter_by(username = form.username.data).first()
            if user is not None and user.verificar_password(form.password.data):
                login_user(user)
                if current_user.is_admin():
                    return redirect("/admin")
                else:
                    return redirect("/usuario")
            else:
                form.username.errors.append("Usuario o contraseña incorrectos")
    return render_template("login.html", form=form)

@app.route("/download/<archivo>")
@login_required
def download(archivo):
    return send_from_directory(app.config["UPLOAD_FOLDER"], archivo)


#---------------------------------------------------------------------------------
@app.route("/admin")
@login_required
def inicio_admin():
    if not current_user.is_admin():
        abort(404)
    else:
        return render_template("inicio_admin.html")

@app.route("/nuevo_user", methods=["get", "post"])
@login_required
def nuevo_user():
    if not current_user.is_admin():
        abort(404)
    else:
        from Plataforma.models import Usuarios
        form = NuevoUserForm()
        if form.validate_on_submit():
            existe_user = Usuarios.query.filter_by(username=form.username.data).first()
            if existe_user is None:
                n_user = Usuarios()
                form.populate_obj(n_user)
                n_user.admin = False
                n_user.creacion = ahora()
                n_user.creado_por = current_user.username
                db.session.add(n_user)
                db.session.commit()
                return redirect("/admin")
            else:
                form.username.errors.append("El usuario ya existe")
        return render_template("nuevo_user.html", form=form)

@app.route("/users", methods=["get", "post"])
@login_required
def users():
    from Plataforma.models import Usuarios
    if not current_user.is_admin():
        abort(404)
    else:
        userss = Usuarios.query.all()
        return render_template("users.html", users=userss)

@app.route("/edit_user/<id>", methods=["get", "post"])
@login_required
def editar_user(id):
    from Plataforma.models import Usuarios
    if not current_user.is_admin():
        abort(404)
    else:
        user1 = Usuarios.query.get(id)
        if user1 is None:
            abort(404)
        else:
            form = NuevoUserForm(obj=user1)
            del form.contrasena
            del form.cont
            if form.validate_on_submit():
                form.populate_obj(user1)
                db.session.commit()
                return redirect("/users")
            else:
                return render_template("edit_user.html", form=form, user=user1)

@app.route("/cambiar_pass/<id>", methods=["get", "post"])
@login_required
def cambiar_pass(id):
    msg = ""
    from Plataforma.models import Usuarios
    if not current_user.is_admin():
        abort(404)
    else:
        user1 = Usuarios.query.get(id)
        if user1 is None:
            abort(404)
        else:
            form = NuevoUserForm()
            del form.nombre
            del form.apellidos
            del form.email
            if form.validate_on_submit():
                del user1.password
                user1.contrasena = form.contrasena.data
                db.session.commit()
                msg = f"La contraseña de {user1.username} se ha cambiado"
            return render_template("cambiar_pass.html", form=form, user=user1, msg=msg)

@app.route("/borrar_user/<id>", methods=["get", "post"])
@login_required
def borrar_user(id):
    from Plataforma.models import Usuarios
    if not current_user.is_admin():
        abort(404)
    else:
        user1 = Usuarios.query.get(id)
        if user1 is None:
            abort(404)
        elif user1.admin == True:
            abort(404)
        else:
            form = ConfirmForm()
            if form.validate_on_submit():
                if form.si.data:
                    db.session.delete(user1)
                    db.session.commit()
                    return redirect("/users")
                else:
                    return redirect("/users")
            return render_template("borrar_user.html", form=form, user=user1)


#---------------------------------------------------------------------------------
@app.route("/usuario")
@login_required
def inicio_user():
    if current_user.is_admin():
        abort(404)
    return render_template("inicio_user.html", user=current_user)

@app.route("/new_actividad", methods=["get", "post"])
@login_required
def new_actividad():
    if current_user.is_admin():
        abort(404)
    else:
        from Plataforma.models import Actividad
        form = NewActividadForm()
        actividades = ("Actividad_Uno", "Actividad_Dos", 
        "Actividad_Tres", "Actividad_Cuatro", "Actividad_Cinco")
        form.activ.choices = actividades
        if form.validate_on_submit():
            try:
                archivo111 = form.arch.data
                nombre = f"{current_user.username}_{form.activ.data}_{ahora()}.rar"
                nombre_archiv = secure_filename(nombre)
                archivo111.save(f"{app.config['UPLOAD_FOLDER']}/{nombre_archiv}")
            except:
                nombre_archiv = ""
            activity = Actividad(user_id=current_user.id, activ=form.activ.data, comentarios=form.comentarios.data,
                archivo=nombre_archiv, creacion=ahora())
            db.session.add(activity)
            db.session.commit()
            return redirect("/usuario")
        else:
            return render_template("new_actividad.html", form=form, user=current_user, creacion=ahora())

@app.route("/actividades/<id>")
@login_required
def actividades_user(id):
    from Plataforma.models import Actividad, Usuarios
    if current_user.is_admin() or str(current_user.id) == id:
        user1 = Usuarios.query.get(id)
        if user1 == None:
            abort(404)
        else:
            activs1 = Actividad.query.filter_by(user_id=id)
    else:
        abort(404)
    return render_template("activs_user.html", activs=activs1, user=user1)


#---------------------------------------------------------------------------------
@app.route("/salir")
def salir():
    logout_user()
    return redirect("/")

@app.errorhandler(404)
def no_encontrado(error):
    return render_template("error.html", error="No se encontro el recurso solicitado")


#----------API_REST--------------------------------------------------------------------------------
@app.route('/api/users', methods=['GET'])
def get_users():
    from Plataforma.models import Usuarios
    users = [user.serialize() for user in Usuarios.query.all() ]
    return jsonify(users)

@app.route('/api/users/<id>', methods=["GET"])
def get_user(id):
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no existe (GET)"})
    return jsonify(user.serialize())

@app.route('/api/users', methods=["POST"])
def crear_user():
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
    # nuevo.creado_por = current_user.username
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.serialize())

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no existe (PUT)"})
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

@app.route('/api/users/<id>', methods=["DELETE"])
def delete_user(id):
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no exite (DELETE)"})
    deleted = user.serialize()
    db.session.delete(user)
    db.session.commit()
    return jsonify(deleted)
    

