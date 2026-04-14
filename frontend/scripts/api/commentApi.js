export async function getCommentsBySubmission(submissionId) {
    const response = await fetch(
        `http://localhost:8000/api/submission/${submissionId}/comment/?id_submission=${submissionId}`
    );
    if (!response.ok) {
        const error = new Error('Error al obtener comentarios');
        error.status = response.status;
        throw error;
    }
    return response.json();
}