const assignmentId = localStorage.getItem('assignment_id');
const subjectName = localStorage.getItem('subject_name');


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
}
