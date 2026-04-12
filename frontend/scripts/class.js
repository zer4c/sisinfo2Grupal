import { openModal, closeModal } from "./modal.js";

const MODAL_ID = "create-assignment-modal";

const subjectName = localStorage.getItem('subject_name');
const subjectCode = localStorage.getItem('subject_code');

document.getElementById('navbar-subject-name').textContent = subjectName;
document.getElementById('banner-subject-name').textContent = subjectName;
document.getElementById('banner-subject-code').textContent = subjectCode;

document.getElementById("btn-open-modal").addEventListener("click", () => openModal(MODAL_ID));
document.getElementById("btn-close-modal").addEventListener("click", () => closeModal(MODAL_ID));
document.getElementById(MODAL_ID).addEventListener("click", (e) => {
  if (e.target === e.currentTarget) closeModal(MODAL_ID);
});

const form = document.getElementById("assignment-form");
const button = document.getElementById("submit-btn");

form.addEventListener("submit", (e) => {
  e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0] || null;

    const data = {
    title: document.getElementById("title").value.trim(),
    description: document.getElementById("description").value.trim() || "",
    due_date: document.getElementById("due_date").value,
    points: Number(document.getElementById("points").value),
    file: file
    };

    console.log('Tarea a crear:', data);

    form.reset();
    closeModal(MODAL_ID);
    showToast('success', 'Tarea creada exitosamente');
});