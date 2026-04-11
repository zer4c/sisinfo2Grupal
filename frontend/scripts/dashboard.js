import { createSubject, getSubjectsByTeacher } from "./api/subjectApi.js";
import { validateForm } from "./formValidator.js";
import { openModal, closeModal } from "./modal.js";

const MODAL_ID = "create-subject-modal";
const TEACHER_ID = 1;

async function loadClasses() {
  const list = document.getElementById("classes-list");
  try {
    const res = await getSubjectsByTeacher(TEACHER_ID);
    const subjects = res.data;

    list.innerHTML = subjects.map(s => `
      <div class="subject-card">
        <div class="subject-card-header">
          <h2>${s.name}</h2>
        </div>
        <div class="subject-card-body">
          <div class="subject-card-row">
            <span class="subject-card-period">${s.period}</span>
            <span class="subject-card-students">#${s.max_students} estudiantes</span>
          </div>
          <span class="subject-card-description">${s.description || 'Sin descripción'}</span>
        </div>
      </div>
    `).join('');

  } catch (err) {
    list.innerHTML = `<p style="color: var(--text-secondary);">No se pudieron cargar las clases.</p>`;
  }
}

document.getElementById("btn-open-modal").addEventListener("click", () => {
  openModal(MODAL_ID);
});
document.getElementById("btn-close-modal").addEventListener("click", () => {
  clearErrors();
  closeModal(MODAL_ID);
});
document.getElementById(MODAL_ID).addEventListener("click", (e) => {
  if (e.target === e.currentTarget) {
    clearErrors();
    closeModal(MODAL_ID);
  }
});

const form = document.getElementById("subject-form");
const message = document.getElementById("message");
const button = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearErrors();

  const data = {
    code: document.getElementById("code").value.trim(),
    name: document.getElementById("name").value.trim(),
    period: document.getElementById("period").value,
    teacher_id: Number(document.getElementById("teacher_id").value),
    max_students: document.getElementById("max_students").value.trim(),
    description: document.getElementById("description").value.trim() || ""
  };

  const errors = validateForm(data);
  if (Object.keys(errors).length > 0) {
    showErrors(errors);
    return;
  }

  try {
    button.disabled = true;
    button.querySelector('.btn-text').textContent = 'Creando...';

    await createSubject({ ...data, max_students: Number(data.max_students) });

    showMessage("¡Clase creada exitosamente!", "success");
    form.reset();
    setTimeout(() => {
      closeModal(MODAL_ID);
      loadClasses();
    }, 1500);

  } catch (err) {
    showMessage("Error al crear la clase. Intenta de nuevo.", "error");
  } finally {
    button.disabled = false;
    button.querySelector('.btn-text').textContent = 'Crear Clase';
  }
});

function showErrors(errors) {
  for (const field in errors) {
    const input = document.getElementById(field);
    if (!input) continue;
    input.classList.add('input-error');
    const errorEl = document.createElement('span');
    errorEl.className = 'field-error';
    errorEl.textContent = errors[field];
    input.parentElement.appendChild(errorEl);
  }
}

function clearErrors() {
  document.querySelectorAll('.field-error').forEach(el => el.remove());
  document.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
}

function showMessage(text, type) {
  message.textContent = text;
  message.className = `message show ${type}`;
  setTimeout(() => message.classList.remove('show'), 5000);
}

loadClasses();