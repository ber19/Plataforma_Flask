let passw = document.getElementById("contrasena")
let passwA = document.getElementById("cont")
let form = document.getElementById("form")
let elem = document.getElementById("flag1")
let elem1 = document.getElementById("guardar")

window.onload = function () {
    form.addEventListener("submit", (e) => {
        if (passw.value != passwA.value) {
            if (!document.getElementById("aviso")) {
                let aviso = document.createElement("p")
                aviso.id = "aviso"
                aviso.classList.add("alert")
                aviso.classList.add("alert-danger")
                let texto = document.createTextNode("Las contraseñas no coinciden")
                aviso.appendChild(texto)
                form.insertBefore(aviso, elem)
            }
            e.preventDefault()
        }
    })
    passw.addEventListener("focus", () => {
        let aviso = document.getElementById("aviso")
        if (aviso) {
            form.removeChild(aviso)
        }
    })
    passwA.addEventListener("focus", () => {
        let aviso = document.getElementById("aviso")
        if (aviso) {
            form.removeChild(aviso)
        }
    })
    passw.addEventListener("keydown", (e) => {
        let mayus = e.getModifierState('CapsLock')
        let aviso = document.getElementById("aviso1")
        if (mayus) {
            if (!aviso) {
                aviso = document.createElement("p")
                aviso.id = "aviso1"
                aviso.classList.add("alert")
                aviso.classList.add("alert-warning")
                let texto = document.createTextNode("Las mayusculas estan activadas")
                aviso.appendChild(texto)
                form.insertBefore(aviso, passwA)
            }
        }
        else {
            if (aviso) {
                form.removeChild(aviso)
            }
        }
    })
    passwA.addEventListener("keydown", (e) => {
        let mayus = e.getModifierState('CapsLock')
        let aviso = document.getElementById("aviso2")
        if (mayus) {
            if (!aviso) {
                aviso = document.createElement("p")
                aviso.id = "aviso2"
                aviso.classList.add("alert")
                aviso.classList.add("alert-warning")
                let texto = document.createTextNode("Las mayusculas estan activadas")
                aviso.appendChild(texto)
                form.insertBefore(aviso, elem1)
            }
        }
        else {
            if (aviso) {
                form.removeChild(aviso)
            }
        }
    })
    passw.addEventListener("blur", () => {
        passw.value = passw.value.trim()
        let aviso = document.getElementById("aviso1")
        if (aviso) {
            form.removeChild(aviso)
        }
    })
    passwA.addEventListener("blur", () => {
        passwA.value = passwA.value.trim()
        let aviso = document.getElementById("aviso2")
        if (aviso) {
            form.removeChild(aviso)
        }
    })
}
