export async function getSubmissionByStudent(studentId, assignmentId) {
    const response = await fetch(`http://localhost:8000/api/submission/student/${studentId}/assignment/${assignmentId}/`);
    if (!response.ok) throw { status: response.status };
    return response.json();
}

export async function getSubmissionsByAssignment(assignmentId) {
  const response = await fetch(`http://localhost:8000/api/submission/${assignmentId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });

  if (!response.ok) {
    const error = new Error("Error al obtener las entregas");
    error.status = response.status;
    throw error;
  }

  return await response.json();
}

export async function createSubmission(data) {
    const response = await fetch('http://localhost:8000/api/submission/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            ...data,
            state_id: 2  // <-- el backend lo requiere en el schema
        })
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Error al crear la entrega');
    }
    return response.json();
}

export async function uploadSubmissionFile(submissionId, file) {
    const ext = file.name.split('.').pop().toLowerCase();

    const formData = new FormData();
    formData.append('submission_data', JSON.stringify({
        submission_id: submissionId,
        type_file: ext
    }));
    formData.append('data', file, file.name);  // el campo debe llamarse "data"

    const response = await fetch(`http://localhost:8000/api/submission/${submissionId}/file`, {
        method: 'POST',
        body: formData
        // NO setear Content-Type manualmente
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Error al subir el archivo');
    }
    return response.json();
}