from flask_script import Manager
from Plataforma.app import app, db
from Plataforma.models import *
from Plataforma.utils import *

manager = Manager(app)


@manager.command
def crear_tablas():
    db.drop_all()
    db.create_all()

@manager.command
def crear_admin():
    administrador = {
        "admin" : True,
        "username" : input("Usuario: ").strip(),
        "contrasena" : passFunc(),
        "nombre" : input("Nombre: ").strip(),
        "apellidos" : input("Apellidos: ").strip(),
        "email": valEmail(),
        "creacion" : ahora(),
        "creado_por" : "ADMIN_MASTER"
    }
    existe_user = Usuarios.query.filter_by(username=administrador["username"]).first()
    if existe_user is None:
        usuario_admin = Usuarios(**administrador)
        db.session.add(usuario_admin)
        db.session.commit()
    else:
        print("El username ya existe")

if __name__ == "__main__":
    manager.run()