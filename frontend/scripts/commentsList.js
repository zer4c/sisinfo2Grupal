import { getCommentsBySubmission } from './api/commentApi.js';

export async function loadComments(submissionId) {
    const container = document.getElementById('comments-container');
    if (!container) return;

    container.innerHTML = '<p class="no-comments">Cargando comentarios...</p>';

    try {
        const response = await getCommentsBySubmission(submissionId);
        const comments = response.data || [];

        if (comments.length === 0) {
            container.innerHTML = '<p class="no-comments">Sin comentarios del docente</p>';
            return;
        }

        container.innerHTML = '';
        comments.forEach(comment => {
            container.appendChild(createCommentItem(comment));
        });
    } catch (error) {
        console.error('Error loading comments:', error);
        container.innerHTML = '<p class="no-comments">Error al cargar comentarios</p>';
    }
}

function createCommentItem(comment) {
    const item = document.createElement('div');
    item.className = 'comment-item';

    const date = new Date(comment.created_at).toLocaleDateString('es-ES', {
        year: 'numeric', month: 'long', day: 'numeric'
    });

    item.innerHTML = `
        <div class="comment-header">
            <span class="comment-author">Docente</span>
            <span class="comment-date">${date}</span>
        </div>
        ${comment.comment ? `<p class="comment-text">${comment.comment}</p>` : ''}
    `;

    return item;
}