let form = document.getElementById("form")
let archivoInput = document.getElementById("arch")
let elem = document.getElementById("flag")

window.onload = function () {
    form.addEventListener("submit", (e) => {
        let filename = archivoInput.value

        let re = /\.rar$|\.zip$/gi
        let res = filename.match(re)

        if (res == null) {
            e.preventDefault()
            if (!document.getElementById("aviso")) {
                let aviso = document.createElement("p")
                aviso.id = "aviso"
                aviso.classList.add("alert")
                aviso.classList.add("alert-danger")
                let texto = document.createTextNode("Debe seleccionar un archivo .zip o .rar")
                aviso.appendChild(texto)
                form.insertBefore(aviso, elem)
                setTimeout(() => {
                    if (document.getElementById("aviso")) {
                        form.removeChild(aviso)
                    }
                }, 4000);
            }
        }
    })
}