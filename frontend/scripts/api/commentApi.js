const BASE = 'http://localhost:8000/api';

export async function getComments(submissionId) {
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/`);
    if (!response.ok) throw { status: response.status };
    return response.json();
}

export async function createComment(submissionId, comment) {
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment })
    });
    if (!response.ok) throw { status: response.status };
    return response.json();
}

export async function updateComment(submissionId, commentId, comment) {
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/${commentId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment })
    });
    if (!response.ok) throw { status: response.status };
    return response.json();
}

export async function deleteComment(submissionId, commentId) {
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/${commentId}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw { status: response.status };
}

export async function addFileToComment(submissionId, commentId, file) {
    const ext = file.name.split('.').pop().toLowerCase();
    const formData = new FormData();
    formData.append('file_type', ext);
    formData.append('file', file, file.name);
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/${commentId}/file`, {
        method: 'POST',
        body: formData
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Error al subir archivo');
    }
    return response.json();
}

export async function getCommentFile(submissionId, commentId, fileId) {
    const response = await fetch(`${BASE}/submission/${submissionId}/comment/${commentId}/file/${fileId}`);
    if (!response.ok) throw { status: response.status };
    return response.blob();
}