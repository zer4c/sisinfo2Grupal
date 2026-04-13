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