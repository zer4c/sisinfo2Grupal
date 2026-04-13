import { enrollStudent } from "./api/subjectApi.js";
import { openModal, closeModal } from "./modal.js";

const JOIN_MODAL_ID = "join-class-modal";
const userId = Number(localStorage.getItem('user_id'));

export function initJoinClass() {
    document.getElementById("btn-join-class").addEventListener("click", () => openModal(JOIN_MODAL_ID));
    document.getElementById("btn-close-join-modal").addEventListener("click", () => closeModal(JOIN_MODAL_ID));
    document.getElementById(JOIN_MODAL_ID).addEventListener("click", (e) => {
        if (e.target === e.currentTarget) closeModal(JOIN_MODAL_ID);
    });

  document.getElementById("btn-confirm-join").addEventListener("click", async () => {
        const code = document.getElementById("join-code").value.trim();
        if (!code) {
        showToast('error', 'Ingresa un código de clase');
        return;
        }

        try {
        const res = await fetch(`http://localhost:8000/api/subject/?code=${code}`);
        if (!res.ok) {
            showToast('error', 'Clase no encontrada');
            return;
        }
        const data = await res.json();
        const subject = data.data[0];

        console.log('userId:', userId);
        console.log('subject.id:', subject.id);

        await enrollStudent(subject.id, userId);

        localStorage.setItem('subject_id', subject.id);
        localStorage.setItem('subject_name', subject.name);
        localStorage.setItem('subject_code', subject.code);

        closeModal(JOIN_MODAL_ID);
        showToast('success', 'Te uniste a la clase exitosamente');
        setTimeout(() => window.location.href = 'class.html', 1500);

    } catch (err) {
        showToast('error', err.message || 'Error al unirse a la clase');
    }
  });
}