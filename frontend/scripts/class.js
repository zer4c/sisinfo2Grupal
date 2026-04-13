import { getAssignmentsBySubject } from './api/assignmentApi.js';

const subjectName = localStorage.getItem('subject_name');
const subjectCode = localStorage.getItem('subject_code');
const subjectId = localStorage.getItem('subject_id');
const role = localStorage.getItem('user_role');

document.getElementById('banner-subject-name').textContent = subjectName;
document.getElementById('banner-subject-code').textContent = subjectCode;

if (role === 'docente') {
  document.getElementById('banner-subject-code').parentElement.style.display = 'block';
  document.getElementById('btn-create-assignment').style.display = 'block';
} else {
  document.getElementById('banner-subject-code').parentElement.style.display = 'none';
  document.getElementById('btn-create-assignment').style.display = 'none';
}

document.getElementById('btn-create-assignment').addEventListener('click', () => {
  window.location.href = 'create-assignment.html';
});

async function loadAssignments() {
  try {
    const assignmentsList = document.getElementById('assignments-list');
    const response = await getAssignmentsBySubject(subjectId);
    const assignments = response.data || [];

    if (!assignments || assignments.length === 0) {
      assignmentsList.innerHTML = '<p class="empty-msg">No hay tareas aún</p>';
      return;
    }

    assignmentsList.innerHTML = '';
    assignments.forEach(assignment => {
      const card = createAssignmentCard(assignment);
      assignmentsList.appendChild(card);
    });
  } catch (error) {
    console.error('Error loading assignments:', error);
    let errorMessage = 'Error al cargar las tareas';
    
    if (error.status === 404) {
      errorMessage = 'No existen tareas';
    }
    
    document.getElementById('assignments-list').innerHTML =
      `<p class="empty-msg">${errorMessage}</p>`;
  }
}

function createAssignmentCard(assignment) {
  const card = document.createElement('div');
  card.className = 'assignment-card';

  const dueDate = new Date(assignment.due_date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  card.innerHTML = `
    <div class="assignment-card-header">
      <h3>${assignment.title}</h3>
    </div>
    <div class="assignment-card-body">
      ${assignment.description ? `<p class="assignment-description">${assignment.description}</p>` : ''}
      <div class="assignment-info">
        <span class="assignment-label">Fecha de entrega:</span>
        <span class="assignment-value">${dueDate}</span>
      </div>
      ${assignment.points ? `
        <div class="assignment-info">
          <span class="assignment-label">Puntuación máxima:</span>
          <span class="assignment-value">${assignment.points} pts</span>
        </div>
      ` : ''}
      <button class="btn-card-action" data-id="${assignment.id}">Ver tarea</button>
    </div>
  `;

  const button = card.querySelector('.btn-card-action');
  button.addEventListener('click', () => {
    localStorage.setItem('assignment_id', assignment.id);
    sessionStorage.setItem(`assignment_${assignment.id}`, JSON.stringify(assignment));
    window.location.href = 'assignment-detail.html';
  });

  return card;
}

loadAssignments();