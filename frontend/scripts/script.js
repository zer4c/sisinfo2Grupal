const API_URL = "http://localhost:8000/api";

async function loadProfesiones() {
  try {
    const response = await fetch(`${API_URL}/profesiones/`);
    const data = await response.json();
    renderTable(data);
  } catch (err) {
    showMessage("No se pudo conectar al servidor", "error");
  }
}

function renderTable(profesiones) {
  const tbody = document.getElementById("profesiones-tbody");
  tbody.innerHTML = "";

  if (profesiones.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="4">No hay profesiones registradas</td></tr>`;
    return;
  }

  profesiones.forEach((profesion) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${profesion.position}</td>
      <td>${profesion.name}</td>
      <td>${profesion.salary}</td>
      <td class="actions">
        <button class="btn-delete" data-id="${profesion.id}">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Asignar eventos a todos los botones eliminar
  document.querySelectorAll(".btn-delete").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = parseInt(btn.dataset.id);
      deleteProfesion(id);
    });
  });
}

async function deleteProfesion(id) {
  try {
    const response = await fetch(`${API_URL}/profesiones/${id}`, {
      method: "DELETE",
    });

    if (response.status === 404) {
      showMessage("La profesión no fue encontrada", "error");
      return;
    }

    if (!response.ok) {
      showMessage("Error al eliminar la profesión", "error");
      return;
    }

    showMessage("Profesión eliminada correctamente", "success");
    loadProfesiones();
  } catch (err) {
    showMessage("No se pudo conectar al servidor", "error");
  }
}

async function createProfesion(name, position, salary) {
  try {
    const response = await fetch(`${API_URL}/profesiones/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, position, salary }),
    });

    const data = await response.json();

    if (response.status === 409) {
      showMessage(data.detail, "warn");
      return;
    }

    if (!response.ok) {
      showMessage("Error al crear la profesión", "error");
      return;
    }

    showMessage("Profesión registrada exitosamente", "success");
    clearForm();
    loadProfesiones();
  } catch (err) {
    showMessage("No se pudo conectar al servidor", "error");
  }
}

let messageTimer = null;

function showMessage(msg, type) {
  const el = document.getElementById("mensaje");
  el.textContent = msg;
  el.className = `${type} visible`;

  if (messageTimer) clearTimeout(messageTimer);
  messageTimer = setTimeout(() => {
    el.className = "";
    el.textContent = "";
  }, 3000);
}

function clearForm() {
  document.getElementById("profesion-name").value = "";
  document.getElementById("profesion-salary").value = "";
  document.getElementById("profesion-pos").value = "";
}

document.getElementById("btn-add").addEventListener("click", () => {
  const name = document.getElementById("profesion-name").value.trim();
  const salary = parseInt(document.getElementById("profesion-salary").value);
  const position = parseInt(document.getElementById("profesion-pos").value);

  if (!name || isNaN(salary) || isNaN(position)) {
    showMessage("Por favor completa todos los campos", "warn");
    return;
  }

  createProfesion(name, position, salary);
});

loadProfesiones();