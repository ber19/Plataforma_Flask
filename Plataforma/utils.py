from getpass import getpass
from datetime import datetime
import re

def passFunc():
    while True:
        contrasena = getpass("Password: ").strip()
        cont = getpass("Password (otra vez): ").strip()
        if contrasena == cont:
            return cont
        else:
            print("Las contraseñas no coinciden. Vuelve a intentarlo")
            continue

def valEmail():
    while True:
        email = input("E-mail: ")
        regex = re.search("^\w+([\.-]?\w+)+@\w+([\.:]?\w+)+(\.[a-zA-Z0-9]{2,3})+$", email)
        if regex:
            return email
        else:
            print("Ingrese un email valido")
            continue

def ahora():
    now1 = datetime.now()
    date_hora = now1.strftime("%d-%m-%Y_%H-%M-%S")
    return date_hora

