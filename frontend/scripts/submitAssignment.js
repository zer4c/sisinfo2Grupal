import { createSubmission, uploadSubmissionFile } from './api/submissionApi.js';

export async function initSubmitSection(userId, assignmentId, currentState) {
    const sidebar = document.getElementById('submit-sidebar');
    if (!sidebar) return;
    
    sidebar.style.display = 'block';

    const btn = document.getElementById('btn-submit-assignment');
    const input = document.getElementById('submit-file-input');

    if (currentState.label !== 'Nuevo') {
        btn.disabled = true;
        btn.textContent = 'Ya entregado';
        input.disabled = true;
        return;
    }

    btn.addEventListener('click', async () => {
        const file = input.files[0];
        if (!file) {
            showToast('error', 'Selecciona un archivo');
            return;
        }

        try {
            btn.disabled = true;
            btn.textContent = 'Entregando...';

            const subRes = await createSubmission({
                student_id: Number(userId),
                assignment_id: Number(assignmentId),
            });
            const submissionId = subRes.data.id;

            await uploadSubmissionFile(submissionId, file);

            showToast('success', 'Tarea entregada exitosamente');
            btn.textContent = 'Ya entregado';
            input.disabled = true;

        } catch (err) {
            console.error(err);
            showToast('error', err.message || 'Error al entregar la tarea');
            btn.disabled = false;
            btn.textContent = 'Entregar';
        }
    });
}