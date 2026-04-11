function showToast(type, message) {
  document.getElementById('toast-global')?.remove();

  const label = type === 'success' ? 'ÉXITO' : 'ERROR';

  const toast = document.createElement('div');
  toast.id = 'toast-global';
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-label">${label}</span>
    <div class="toast-divider"></div>
    <span class="toast-msg">${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;

  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}