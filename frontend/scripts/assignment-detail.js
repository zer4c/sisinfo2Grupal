import { getAssignmentFiles, getAssignmentFile } from './api/assignmentApi.js';
import { getAssignmentState, createStateBadge } from './assignmentState.js';
import { getSubmissionsByAssignment } from './api/submissionApi.js';
import { getStudentById } from './api/studentApi.js';
import { initSubmitSection } from './submitAssignment.js';
import { getComments, createComment, updateComment, deleteComment, addFileToComment, getCommentFile } from './api/commentApi.js';
const assignmentId = localStorage.getItem('assignment_id');
const subjectName = localStorage.getItem('subject_name');
const userId = localStorage.getItem('user_id');
const role = localStorage.getItem('user_role');

const assignmentData = JSON.parse(sessionStorage.getItem(`assignment_${assignmentId}`));

if (!assignmentData) {
    document.body.innerHTML = '<p style="padding: 20px; text-align: center;">Error: No se pudo cargar la información de la tarea</p>';
} else {

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    document.getElementById('detail-title').textContent = assignmentData.title;
    document.getElementById('detail-subject').textContent = `Clase: ${subjectName}`;
    document.getElementById('detail-title-value').textContent = assignmentData.title;
    document.getElementById('detail-points').textContent = `${assignmentData.points} pts`;
    document.getElementById('detail-created-at').textContent = formatDate(assignmentData.created_at);
    document.getElementById('detail-due-date').textContent = formatDate(assignmentData.due_date);

    const descriptionEl = document.getElementById('detail-description');
    if (assignmentData.description) {
        descriptionEl.innerHTML = `<p>${assignmentData.description}</p>`;
    } else {
        descriptionEl.innerHTML = '<p class="no-info">Sin descripción</p>';
    }

    document.querySelector('.btn-card-action').href = 'class.html';

    loadFiles();
    if (role === 'docente') {
        document.getElementById('submissions-sidebar').style.display = 'block';
        loadSubmissions()
    }

    if (role === 'estudiante' && userId) {
        loadEstudiante();
    }
}

let activeSubmissionId = null;

document.getElementById('btn-close-comment-modal').addEventListener('click', () => {
    document.getElementById('comment-modal').style.display = 'none';
    document.getElementById('comments-container').innerHTML = '';
    document.getElementById('comment-input').value = '';
    document.getElementById('comment-file-input').value = '';
    activeSubmissionId = null;
});

function openCommentModal(submissionId) {
    activeSubmissionId = submissionId;
    document.getElementById('comment-modal').style.display = 'flex';
    loadComments(submissionId);
}

async function loadComments(submissionId) {
    const container = document.getElementById('comments-container');
    try {
        const res = await getComments(submissionId);
        const comments = res.data || [];
        container.innerHTML = '';
        if (comments.length === 0) {
            container.innerHTML = '<p class="no-comments">No hay comentarios aún.</p>';
            return;
        }
        comments.forEach(c => container.appendChild(createCommentEl(c, submissionId)));
    } catch {
        container.innerHTML = '<p class="no-comments">Error al cargar comentarios.</p>';
    }
}

function createCommentEl(comment, submissionId) {
    const el = document.createElement('div');
    el.className = 'comment-item';
    el.dataset.id = comment.id;

    const dots = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    dots.setAttribute('viewBox', '0 0 24 24');
    dots.setAttribute('width', '16');
    dots.setAttribute('height', '16');
    dots.setAttribute('fill', 'currentColor');
    dots.classList.add('comment-dots');
    dots.innerHTML = `<circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>`;

    const menu = document.createElement('div');
    menu.className = 'comment-menu';
    menu.style.display = 'none';
    menu.innerHTML = `
        <button class="comment-menu-btn" data-action="edit">Editar</button>
        <button class="comment-menu-btn" data-action="delete">Eliminar</button>
    `;

    dots.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.style.display = menu.style.display === 'none' ? 'flex' : 'none';
    });

    document.addEventListener('click', () => { menu.style.display = 'none'; }, { once: true });

    menu.querySelector('[data-action="edit"]').addEventListener('click', async () => {
        const newText = prompt('Editar comentario:', comment.comment || '');
        if (newText === null) return;
        try {
            await updateComment(submissionId, comment.id, newText);
            showToast('success', 'Comentario actualizado.');
            loadComments(submissionId);
        } catch {
            showToast('error', 'No se pudo actualizar el comentario.');
        }
    });

    menu.querySelector('[data-action="delete"]').addEventListener('click', async () => {
        try {
            await deleteComment(submissionId, comment.id);
            showToast('success', 'Comentario eliminado.');
            loadComments(submissionId);
        } catch {
            showToast('error', 'No se pudo eliminar el comentario.');
        }
    });

    const dotsWrapper = document.createElement('div');
    dotsWrapper.className = 'comment-dots-wrapper';
    dotsWrapper.appendChild(dots);
    dotsWrapper.appendChild(menu);

    const body = document.createElement('div');
    body.className = 'comment-body';

    if (comment.comment) {
        const text = document.createElement('p');
        text.className = 'comment-text';
        text.textContent = comment.comment;
        body.appendChild(text);
    }

    if (comment.files && comment.files.length > 0) {
        comment.files.forEach((file, index) => {
            const fileEl = document.createElement('div');
            fileEl.className = 'comment-file-item';
            fileEl.innerHTML = `
                <span class="file-name">archivo${index + 1}.${file.type_file}</span>
                <button class="btn-download comment-file-download">Descargar</button>
            `;
            fileEl.querySelector('.comment-file-download').addEventListener('click', async () => {
                try {
                    const blob = await getCommentFile(submissionId, comment.id, file.id);
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `archivo${index + 1}.${file.type_file}`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } catch {
                    showToast('error', 'No se pudo descargar el archivo.');
                }
            });
            body.appendChild(fileEl);
        });
    }

    const date = document.createElement('span');
    date.className = 'comment-date';
    date.textContent = new Date(comment.created_at).toLocaleDateString('es-ES');

    el.appendChild(dotsWrapper);
    el.appendChild(body);
    el.appendChild(date);

    return el;
}

document.getElementById('btn-send-comment').addEventListener('click', async () => {
    if (!activeSubmissionId) return;
    const text = document.getElementById('comment-input').value.trim();
    const file = document.getElementById('comment-file-input').files[0];

    if (!text && !file) {
        showToast('error', 'Escribe un comentario o adjunta un archivo.');
        return;
    }

    if (!file && text.length === 0) {
    showToast('error', 'El comentario no puede estar vacío.');
    return;
}

    try {
        const res = await createComment(activeSubmissionId, text || null);
        const commentId = res.data.id;

         if (file) {
            try {
                await addFileToComment(activeSubmissionId, commentId, file);
            } catch (err) {
                console.error('Error subiendo file:', err);
                showToast('error', 'Comentario enviado pero el archivo falló.');
            }
        }

        document.getElementById('comment-input').value = '';
        document.getElementById('comment-file-input').value = '';
        showToast('success', 'Comentario enviado.');
        loadComments(activeSubmissionId);
    } catch {
        showToast('error', 'Error al enviar el comentario.');
    }
});

async function loadEstudiante() {
    const state = await getAssignmentState(userId, assignmentId);
    loadAssignmentState(state);
    initSubmitSection(userId, assignmentId, state);
    await loadStudentComments();
}

async function loadStudentComments() {
    try {
        const { getSubmissionByStudent } = await import('./api/submissionApi.js');
        const res = await getSubmissionByStudent(userId, assignmentId);
        const submission = res.data;
        if (!submission) return;

        document.getElementById('student-comments-section').style.display = 'block';
        const list = document.getElementById('student-comments-list');

        const commentsRes = await getComments(submission.id);
        const comments = commentsRes.data || [];

        if (comments.length === 0) {
            list.innerHTML = '<p class="no-files">No hay comentarios</p>';
            return;
        }

        list.innerHTML = '';
        comments.forEach((c, index) => {
            const item = document.createElement('div');
            item.className = 'comment-item';

            if (c.comment) {
                const text = document.createElement('p');
                text.className = 'comment-text';
                text.textContent = c.comment;
                item.appendChild(text);
            }

            if (c.files && c.files.length > 0) {
                c.files.forEach((file, fi) => {
                    const fileEl = document.createElement('div');
                    fileEl.className = 'comment-file-item';
                    fileEl.innerHTML = `
                        <span class="file-name">archivo${fi + 1}.${file.type_file}</span>
                        <button class="btn-download student-file-download">Descargar</button>
                    `;
                    fileEl.querySelector('.student-file-download').addEventListener('click', async () => {
                        try {
                            const blob = await getCommentFile(submission.id, c.id, file.id);
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `archivo${fi + 1}.${file.type_file}`;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                            document.body.removeChild(a);
                        } catch {
                            showToast('error', 'No se pudo descargar el archivo.');
                        }
                    });
                    item.appendChild(fileEl);
                });
            }

            const date = document.createElement('span');
            date.className = 'comment-date';
            date.textContent = new Date(c.created_at).toLocaleDateString('es-ES');
            item.appendChild(date);

            list.appendChild(item);
        });
    } catch (err) {
        console.error('Error cargando comentarios del estudiante:', err);
    }
}

async function loadAssignmentState(state) {
    try {
        const badge = createStateBadge(state);
        const detailSection = document.querySelector('.detail-section');
        if (!detailSection) return;
        const h2 = detailSection.querySelector('h2');
        if (!h2 || document.querySelector('.section-header')) return;

        h2.style.cssText = 'display:flex; justify-content:space-between; align-items:center; width:100%';
        const stateSpan = document.createElement('span');
        stateSpan.innerHTML = badge;
        h2.appendChild(stateSpan);
    } catch (error) {
        console.error('Error loading assignment state:', error);
    }
}

async function loadFiles() {
    try {
        const response = await getAssignmentFiles(assignmentId);
        const files = response.data || [];
        const filesList = document.getElementById('files-list');

        if (!files || files.length === 0) {
            filesList.innerHTML = '<p class="no-files">No hay archivos</p>';
            return;
        }

        filesList.innerHTML = '';
        files.forEach((file, index) => {
            const fileItem = createFileItem(file, index);
            filesList.appendChild(fileItem);
        });
    } catch (error) {
        console.error('Error loading files:', error);
        document.getElementById('files-list').innerHTML = '<p class="no-files">Error al cargar archivos</p>';
    }
}

function createFileItem(file, index) {
    const item = document.createElement('div');
    item.className = 'file-item';
    console.log(file);

    const fileName = document.createElement('span');
    fileName.className = 'file-name';
    fileName.textContent = `archivo${index + 1}.${file.type_file}`;

    const downloadBtn = document.createElement('button');
    downloadBtn.className = 'btn-download';
    downloadBtn.textContent = 'Ver';

    downloadBtn.addEventListener('click', async () => {
        try {
            const blob = await getAssignmentFile(assignmentId, file.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `archivo${index + 1}.${file.type_file}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Error downloading file:', error);
        }
    });

    item.appendChild(fileName);
    item.appendChild(downloadBtn);

    return item;
}

async function loadSubmissions() {
    try {
        const response = await getSubmissionsByAssignment(assignmentId);
        const submissions = response.data || [];
        const submissionsList = document.getElementById('submissions-list');

        if (!submissions || submissions.length === 0) {
            submissionsList.innerHTML = '<p class="no-submissions">No hay entregas</p>';
            return;
        }

        submissionsList.innerHTML = '';

        for (const submission of submissions) {
            try {
                const studentResponse = await getStudentById(submission.student_id);
                submission.student = studentResponse.data;
            } catch (err) {
                console.error(`Error getting student ${submission.student_id}:`, err);
                submission.student = null;
            }

            const item = createSubmissionItem(submission);
            submissionsList.appendChild(item);
        }
    } catch (error) {
        console.error('Error loading submissions:', error);
        let errorMessage = 'Error al cargar entregas';
        if (error.status === 404) {
            errorMessage = 'No hay entregas';
        }
        document.getElementById('submissions-list').innerHTML = `<p class="no-submissions">${errorMessage}</p>`;
    }
}

function createSubmissionItem(submission) {
    const item = document.createElement('div');
    item.className = 'submission-item';

    const studentName = document.createElement('div');
    studentName.className = 'submission-student-name';
    const name = submission.student && submission.student.name
        ? submission.student.name
        : `Estudiante #${submission.student_id}`;
    studentName.textContent = name;

    const meta = document.createElement('div');
    meta.className = 'submission-meta';

    meta.innerHTML = `<span>Estado: ${submission.state_id === 2 ? 'Entregado' : 'Pendiente'}</span>`;

    if (submission.grade !== null && submission.grade !== undefined) {
        const gradeSpan = document.createElement('span');
        gradeSpan.textContent = `Calificación: ${submission.grade}`;
        meta.appendChild(gradeSpan);
    }

    const commentBtn = document.createElement('button');
    commentBtn.className = 'btn-card-action';
    commentBtn.textContent = 'Comentarios';
    commentBtn.addEventListener('click', () => openCommentModal(submission.id));

    item.appendChild(studentName);
    item.appendChild(meta);
    item.appendChild(commentBtn);

    return item;
}
