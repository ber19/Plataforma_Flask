let email = document.getElementById("email")
let elem = document.getElementById("cCont")

window.onload = function () {
    form.addEventListener("submit", (e) => {
        let emailVal = email.value
        let re = /^\w+([\.-]?\w+)+@\w+([\.:]?\w+)+(\.[a-zA-Z0-9]{2,3})+$/g
        let res = emailVal.match(re)
        if (res == null && emailVal.length != 0) {
            if (!document.getElementById("aviso")) {
                let aviso = document.createElement("p")
                aviso.id = "aviso"
                aviso.classList.add("alert")
                aviso.classList.add("alert-danger")
                let texto = document.createTextNode("Introduzca un correo valido")
                aviso.appendChild(texto)
                form.insertBefore(aviso, elem)
            }
            e.preventDefault()
        }
    })
    email.addEventListener("focus", () => {
        let aviso = document.getElementById("aviso")
        if (aviso) {
            form.removeChild(aviso)
        }
    })
}