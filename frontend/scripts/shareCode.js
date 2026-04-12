import { openModal, closeModal } from "./modal.js";

const SHARE_MODAL_ID = "share-code-modal";

export function initShareModal() {
  document.getElementById("btn-close-share-modal").addEventListener("click", () => closeModal(SHARE_MODAL_ID));

  document.getElementById(SHARE_MODAL_ID).addEventListener("click", (e) => {
    if (e.target === e.currentTarget) closeModal(SHARE_MODAL_ID);
  });

  document.getElementById("btn-copy-code").addEventListener("click", () => {
    const code = document.getElementById("share-code-text").textContent;
    navigator.clipboard.writeText(code).then(() => {
      showToast('success', 'Código copiado al portapapeles');
    });
  });
}

export function openShareModal(code) {
  document.getElementById("share-code-text").textContent = code;
  openModal(SHARE_MODAL_ID);
}