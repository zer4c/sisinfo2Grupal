import { createSubmission, uploadSubmissionFile, getSubmissionByStudent } from './api/submissionApi.js';

export async function initSubmitSection(userId, assignmentId, currentState) {
    const sidebar = document.getElementById('submit-sidebar');
    if (!sidebar) return;

    sidebar.style.display = 'block';

    const btn = document.getElementById('btn-submit-assignment');
    const input = document.getElementById('submit-file-input');
    const preview = document.getElementById('submit-file-preview');

    if (currentState.label !== 'Nuevo') {
        btn.disabled = true;
        btn.textContent = 'Ya entregado';
        input.disabled = true;
        return;
    }

    function actualizarBadge() {
        const detailSection = document.querySelector('.detail-section');
        if (!detailSection) return;
        const h2 = detailSection.querySelector('h2');
        if (!h2) return;
        const span = h2.querySelector('.assignment-state');
        if (span) {
            span.className = 'assignment-state state-entregado';
            span.textContent = 'Entregado';
        }
    }

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (!file) {
            preview.innerHTML = '';
            return;
        }
        preview.innerHTML = `
            <div class="submit-file-item">
                <span class="submit-file-name">${file.name}</span>
                <span style="font-size:12px; color:var(--text-secondary)">${(file.size / 1024).toFixed(1)} KB</span>
            </div>
        `;
    });

    btn.addEventListener('click', async () => {
        const file = input.files[0];
        if (!file) {
            showToast('error', 'Selecciona un archivo');
            return;
        }

        try {
            btn.disabled = true;
            btn.textContent = 'Entregando...';

            try {
                const existing = await getSubmissionByStudent(userId, assignmentId);
                if (existing.data) {
                    showToast('error', 'Ya entregaste esta tarea');
                    btn.textContent = 'Ya entregado';
                    input.disabled = true;
                    return;
                }
            } catch (e) {
                // si falla la verificación continuar igual
            }

            const subRes = await createSubmission({
                student_id: Number(userId),
                assignment_id: Number(assignmentId),
            });
            const submissionId = subRes.data.id;

            await uploadSubmissionFile(submissionId, file);

            showToast('success', 'Tarea entregada exitosamente');
            btn.textContent = 'Ya entregado';
            input.disabled = true;
            actualizarBadge();  // <-- aquí

        } catch (err) {
            console.error(err);
            showToast('error', err.message || 'Error al entregar la tarea');
            btn.disabled = false;
            btn.textContent = 'Entregar';
        }
    });
}