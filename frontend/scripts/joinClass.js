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

      await enrollStudent(subject.id, userId);

      closeModal(JOIN_MODAL_ID);
      showToast('success', 'Te uniste a la clase exitosamente');

    } catch (err) {
      showToast('error', err.message || 'Error al unirse a la clase');
    }
  });
}