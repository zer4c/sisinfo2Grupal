export function openModal(modalId) {
  document.getElementById(modalId).classList.add('show');
}

export function closeModal(modalId) {
  document.getElementById(modalId).classList.remove('show');
}