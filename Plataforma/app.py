from flask import Flask, render_template, redirect, \
    abort
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

#---------------------------------------------------------------------------------
@app.route("/usuario")
@login_required
def inicio_user():
    if current_user.is_admin():
        abort(404)
    return render_template("inicio_user.html")

#---------------------------------------------------------------------------------
@app.route("/salir")
def salir():
    logout_user()
    return redirect("/")

@app.errorhandler(404)
def no_encontrado(error):
    return render_template("error.html", error="No se encontro el recurso solicitado")

