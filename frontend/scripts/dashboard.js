import { initJoinClass } from "./joinClass.js";
import { createSubject, getSubjectsByTeacher, getSubjectsByStudent } from "./api/subjectApi.js";
import { validateForm } from "./formValidator.js";
import { openModal, closeModal } from "./modal.js";
import { initShareModal, openShareModal } from "./shareCode.js";

const MODAL_ID = "create-subject-modal";
const USER_ID = Number(localStorage.getItem('user_id'));
const USER_ROLE = localStorage.getItem('user_role');

async function renderClassCards(subjects, isTeacher = true) {
  const list = document.getElementById("classes-list");

  list.innerHTML = subjects.map(s => {
    const shareButton = isTeacher
      ? `<button class="btn-card-action btn-share" data-code="${s.code}">Compartir código</button>`
      : '';

    return `
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
          ${shareButton}
          <button class="btn-card-action btn-view" data-id="${s.id}" data-name="${s.name}" data-code="${s.code}">Ver clase</button>
        </div>
      </div>
    `;
  }).join('');


  document.querySelectorAll('.btn-share').forEach(btn => {
    btn.addEventListener('click', () => openShareModal(btn.dataset.code));
  });

  document.querySelectorAll('.btn-view').forEach(btn => {
    btn.addEventListener('click', () => {
      localStorage.setItem('subject_id', btn.dataset.id);
      localStorage.setItem('subject_name', btn.dataset.name);
      localStorage.setItem('subject_code', btn.dataset.code);
      window.location.href = 'class.html';
    });
  });
}

async function loadClasses() {
  const list = document.getElementById("classes-list");
  try {
    let res;
    if (USER_ROLE === 'docente') {
      res = await getSubjectsByTeacher(USER_ID);
    } else {
      res = await getSubjectsByStudent(USER_ID);
    }

    const subjects = res.data;
    await renderClassCards(subjects, USER_ROLE === 'docente');
  } catch (err) {
    list.innerHTML = `<p style="color: var(--text-secondary);">No se pudieron cargar las clases</p>`;
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
const button = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearErrors();

  const data = {
    code: document.getElementById("code").value.trim(),
    name: document.getElementById("name").value.trim(),
    period: document.getElementById("period").value,
    teacher_id: Number(localStorage.getItem('user_id')),
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

    form.reset();
    setTimeout(() => {
      closeModal(MODAL_ID);
      showToast('success', 'Clase creada exitosamente.');
      loadClasses();
    }, 1500);

  } catch (err) {
    showToast('error', err.message || 'Error al crear la clase.');
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

initShareModal();


if (USER_ROLE === 'docente') {
  document.getElementById('btn-open-modal').style.display = 'block';
  loadClasses();
} else {
  document.getElementById('btn-open-modal').style.display = 'none';
  document.getElementById('btn-join-class').style.display = 'block';
  loadClasses();
  initJoinClass();
}
