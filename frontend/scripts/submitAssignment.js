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

    const files = [];
    const allowed = ['pdf', 'docx', 'xlsx', 'zip', 'jpg', 'png'];

    function renderFiles() {
        preview.innerHTML = files.map((f, i) => `
            <div class="submit-file-item" style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px;">
                <span class="submit-file-name" style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${f.name}</span>
                <span style="font-size:12px;color:var(--text-secondary);white-space:nowrap">${(f.size / 1024).toFixed(1)} KB</span>
                <button class="file-item-remove" data-index="${i}" style="background:none;border:none;cursor:pointer;font-size:14px;color:var(--text-secondary);padding:0 4px;flex-shrink:0">✕</button>
            </div>
        `).join('');

        preview.querySelectorAll('.file-item-remove').forEach(btn => {
            btn.addEventListener('click', () => {
                files.splice(Number(btn.dataset.index), 1);
                input.value = '';
                renderFiles();
            });
        });
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
        if (!file) return;

        const ext = file.name.split('.').pop().toLowerCase();
        if (!allowed.includes(ext)) {
            showToast('error', 'Tipo de archivo no permitido');
            input.value = '';
            return;
        }

        files.push(file);
        input.value = ''; // permite volver a seleccionar el mismo archivo
        renderFiles();
    });

    btn.addEventListener('click', async () => {
        if (files.length === 0) {
            showToast('error', 'Selecciona al menos un archivo');
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
                state_id: 2,
            });
            const submissionId = subRes.data.id;

            for (const file of files) {
                await uploadSubmissionFile(submissionId, file);
            }

            showToast('success', 'Tarea entregada exitosamente');
            btn.textContent = 'Ya entregado';
            input.disabled = true;
            preview.querySelectorAll('.file-item-remove').forEach(b => b.remove());

            actualizarBadge();

        } catch (err) {
            console.error(err);
            showToast('error', err.message || 'Error al entregar la tarea');
            btn.disabled = false;
            btn.textContent = 'Entregar';
        }
    });
}