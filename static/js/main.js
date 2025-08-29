document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.django-message').forEach(msg => {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${msg.dataset.level} border-0`;
    toast.setAttribute('role','alert');
    toast.setAttribute('aria-live','assertive');
    toast.setAttribute('aria-atomic','true');
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${msg.innerHTML}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>`;
    document.getElementById('toast-stack').appendChild(toast);
    new bootstrap.Toast(toast, { delay: 4000 }).show();
    msg.remove();
  });
});