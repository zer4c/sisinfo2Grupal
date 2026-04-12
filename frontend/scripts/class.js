const subjectName = localStorage.getItem('subject_name');
const subjectCode = localStorage.getItem('subject_code');
const subjectId = localStorage.getItem('subject_id');

document.getElementById('banner-subject-name').textContent = subjectName;
document.getElementById('banner-subject-code').textContent = subjectCode;

document.getElementById('btn-create-assignment').addEventListener('click', () => {
  window.location.href = 'create-assignment.html';
});