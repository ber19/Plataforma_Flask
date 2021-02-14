from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[Required()])
    password = PasswordField("Contraseña: ", validators=[Required()])
    enviar = SubmitField("Entrar")

class NuevoUserForm(FlaskForm):
    username = StringField("Username:", validators=[Required()])
    contrasena = PasswordField("Contraseña:", validators=[Required()])
    cont = PasswordField("Repita la contraseña:", validators=[Required()])
    nombre = StringField("Nombre:", validators=[Required()])
    apellidos = StringField("Apellidos:", validators=[Required()])
    email = EmailField("E-mail:", validators=[Required()])
    enviar = SubmitField("Registrar")
    guardar = SubmitField("Guardar")
