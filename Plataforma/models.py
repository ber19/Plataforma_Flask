from sqlalchemy import Boolean, Column, ForeignKey, \
    Integer, String
from sqlalchemy.orm import relationship
from Plataforma.app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__="Usuarios"
    id = Column(Integer, primary_key=True)
    admin = Column(Boolean, default=False)
    username = Column(String(100), nullable=False)
    password = Column(String(150), nullable=False)
    nombre = Column(String(150))
    apellidos = Column(String(150))
    email = Column(String(150))
    creacion = Column(String(100))
    creado_por = Column(String(100))
    actividades = relationship("Actividad", cascade="all, delete-orphan",
    backref="user111", lazy="dynamic")

    def __repr__(self):
        return (f'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    @property
    def contrasena(self):
        raise AttributeError("contrasena no es un atributo leible")
    @contrasena.setter
    def contrasena(self, contrasena111):
        self.password = generate_password_hash(contrasena111)
    def verificar_password(self, contrasena222):
        return check_password_hash(self.password, contrasena222)

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
    def is_admin(self):
        return self.admin

class Actividad(db.Model):
    __tablename__ = "actividad"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=False)
    activ = Column(String(50), nullable=False)
    comentarios = Column(String(300))
    archivo = Column(String(150))
    creacion = Column(String(100))

    def __repr__(self):
        return (f'<{self.__class__.__name__}: {self.id}>'.format(self=self))