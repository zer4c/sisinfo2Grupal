import { createAssignment } from "./api/assignmentApi.js";

const subjectId = localStorage.getItem('subject_id');
const files = [];

document.getElementById('btn-back').addEventListener('click', () => {
  window.location.href = 'class.html';
});

document.getElementById('file-input').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) addFile(file);
});

function addFile(file) {
  const allowed = ['pdf', 'docx', 'xlsx', 'zip', 'jpg', 'png'];
  const ext = file.name.split('.').pop().toLowerCase();

  if (!allowed.includes(ext)) {
    showToast('error', 'Tipo de archivo no permitido');
    return;
  }

  files.push(file);
  renderFiles();
}

function renderFiles() {
  const list = document.getElementById('file-list');
  list.innerHTML = files.map((f, i) => `
    <div class="file-item">
      <span class="file-item-name">${f.name}</span>
      <button class="file-item-remove" data-index="${i}">✕</button>
    </div>
  `).join('');

  document.querySelectorAll('.file-item-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      files.splice(Number(btn.dataset.index), 1);
      renderFiles();
    });
  });
}

document.getElementById('btn-submit').addEventListener('click', async () => {
  const title = document.getElementById('title').value.trim();
  const description = document.getElementById('description').value.trim();
  const due_date = document.getElementById('due_date').value;
  const points = document.getElementById('points').value;

  if (!title || !due_date || !points) {
    showToast('error', 'Completa los campos requeridos');
    return;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const selected = new Date(due_date);

  if (selected < today) {
    showToast('error', 'La fecha de entrega no puede ser en el pasado');
    return;
  }

  const data = {
    subject_id: Number(subjectId),
    title,
    description: description || null,
    due_date,
    points: Number(points)
  };

  try {
    await createAssignment(data);
    showToast('success', 'Tarea creada exitosamente');
    setTimeout(() => window.location.href = 'class.html', 1500);
  } catch (err) {
    showToast('error', err.message || 'Error al crear la tarea');
  }
});