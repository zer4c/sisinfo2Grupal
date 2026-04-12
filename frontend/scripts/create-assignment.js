const subjectId = localStorage.getItem('subject_id');
const files = [];


document.getElementById('btn-back').addEventListener('click', () => {
  window.location.href = 'class.html';
});


document.getElementById('file-input').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) addFile(file);
});


const uploadArea = document.getElementById('file-upload-area');

uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
  uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
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
  previewFile(file);
}

function previewFile(file) {
  const preview = document.getElementById('preview-area');
  const ext = file.name.split('.').pop().toLowerCase();
  const url = URL.createObjectURL(file);

  if (['jpg', 'png'].includes(ext)) {
    preview.innerHTML = `<img src="${url}" alt="${file.name}" />`;
  } else if (ext === 'pdf') {
    preview.innerHTML = `<iframe src="${url}"></iframe>`;
  } else {
    preview.innerHTML = `<span class="preview-unsupported">📄 ${file.name}<br>Sin previsualización disponible</span>`;
  }
}

function renderFiles() {
  const list = document.getElementById('file-list');
  list.innerHTML = files.map((f, i) => `
    <div class="file-item" data-index="${i}">
      <span class="file-item-name">${f.name}</span>
      <button class="file-item-remove" data-index="${i}">✕</button>
    </div>
  `).join('');

  document.querySelectorAll('.file-item').forEach(item => {
    item.addEventListener('click', (e) => {
      if (e.target.classList.contains('file-item-remove')) return;
      previewFile(files[Number(item.dataset.index)]);
    });
  });

  document.querySelectorAll('.file-item-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      files.splice(Number(btn.dataset.index), 1);
      renderFiles();
      document.getElementById('preview-area').innerHTML = `<span class="preview-placeholder">Selecciona un archivo para previsualizarlo</span>`;
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

  const data = {
    subject_id: Number(subjectId),
    title,
    description: description || "",
    due_date,
    points: Number(points),
  };

  console.log('Tarea a crear:', data);
  console.log('Archivos:', files);

  showToast('success', 'Tarea creada exitosamente');
  setTimeout(() => window.location.href = 'class.html', 1500);
});