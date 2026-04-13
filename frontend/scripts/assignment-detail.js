import { getAssignmentFiles, getAssignmentFile } from './api/assignmentApi.js';
import { getSubmissionsByAssignment } from './api/submissionApi.js';
import { getStudentById } from './api/studentApi.js';

const assignmentId = localStorage.getItem('assignment_id');
const subjectName = localStorage.getItem('subject_name');
const userRole = localStorage.getItem('user_role');

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

    if (userRole === 'docente') {
        loadFiles();
        loadSubmissions();
    } else {
        document.querySelector('.assignment-detail-sidebar-right').style.display = 'none';
        loadFiles();
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

    item.appendChild(studentName);
    item.appendChild(meta);

    return item;
}
