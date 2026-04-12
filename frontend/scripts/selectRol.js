let selectedRole = null;

document.getElementById('btn-docente').addEventListener('click', () => {
    selectedRole = 'docente';
    document.getElementById('btn-docente').classList.add('active');
    document.getElementById('btn-estudiante').classList.remove('active');
});

document.getElementById('btn-estudiante').addEventListener('click', () => {
    selectedRole = 'estudiante';
    document.getElementById('btn-estudiante').classList.add('active');
    document.getElementById('btn-docente').classList.remove('active');
});

document.getElementById('btn-confirm').addEventListener('click', async () => {
    if (!selectedRole) {
        showToast('error', 'Selecciona un rol para continuar');
        return;
    }

    const id = document.getElementById('user-id').value.trim();
    if (!id || Number(id) < 1) {
        showToast('error', 'Ingresa un ID válido');
        return;
    }

    try {
        const endpoint = selectedRole === 'docente' ? 'teacher' : 'student';
        const response = await fetch(`http://localhost:8000/api/${endpoint}/${id}/`);

        if (!response.ok) {
            showToast('error', 'El ID no existe, verifica e intenta de nuevo');
            return;
        }

        localStorage.setItem('user_id', Number(id));
        localStorage.setItem('user_role', selectedRole);

        if (selectedRole === 'docente') {
            window.location.href = 'pages/teacher-dashboard.html';
        } else {
            window.location.href = 'pages/student-dashboard.html';
        }

    } catch (err) {
        showToast('error', 'Error al conectar con el servidor');
    }
});