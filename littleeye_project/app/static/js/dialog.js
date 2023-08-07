/* bootstrap modal dialog*/
; (function () {

    const modal = new bootstrap.Modal('#modal');
    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "dialog") {
            modal.show()
        }
    })

    htmx.on('htmx:beforeSwap', (e) => {
        if (e.detail.target.id === "dialog" && !e.detail.xhr.response) {
            modal.hide()
            e.detail.shouldSwap = false;
        }
    })

    htmx.on("hidden.bs.modal", (e) => {
        // wenn modal mit id dialog geschlossen wird, modal auf leer setzen
        document.getElementById("dialog").innerHTML = "";
    })
})()
