const API = "http://localhost:8000/profesion";

document.getElementById("form-profesion").addEventListener("submit", async (e) => {
    e.preventDefault();

    const body = {
        name: document.getElementById("nombre").value,
        position: parseInt(document.getElementById("posicion").value),
        salary: parseFloat(document.getElementById("sueldo").value),
    };

    const msg = document.getElementById("mensaje");

    try {
        const res = await fetch(API + "/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const data = await res.json();

        if (data.ok) {
            msg.textContent = data.message;
            msg.className = "mensaje exito";
            e.target.reset();
        } else {
            msg.textContent = data.message ?? "An unexpected error occurred.";
            msg.className = "mensaje error";
        }
    } catch (_) {
        msg.textContent = "Could not connect to the server.";
        msg.className = "mensaje error";
    }

    setTimeout(() => (msg.className = "mensaje oculto"), 3000);
});