export async function getAssignmentsBySubject(subjectId) {
  const response = await fetch(`http://localhost:8000/api/assignment/?subject_id=${subjectId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al obtener las tareas");
  }

  return await response.json();
}

export async function createAssignment(data) {
  const response = await fetch("http://localhost:8000/api/assignment/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al crear la tarea");
  }

  return await response.json();
}

export async function uploadAssignmentFile(assignment_id, file) {
  const ext = file.name.split('.').pop().toLowerCase();

  const formData = new FormData();


  const payload = {
    assignment_id: parseInt(assignment_id),
    type_file: ext
  };
  formData.append('assignment_data', JSON.stringify(payload));


  formData.append('data', file, file.name);

  const response = await fetch(`http://localhost:8000/api/assignment/${assignment_id}/file`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const err = await response.json();
    console.log(JSON.stringify(err, null, 2));
    throw new Error(err.detail || "Error al subir el archivo");
  }

  return await response.json();
}

export async function getAssignmentFiles(assignmentId) {
  const response = await fetch(`http://localhost:8000/api/assignment/${assignmentId}/file/`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al obtener los archivos");
  }

  return await response.json();
}

export async function getAssignmentFile(assignmentId, fileId) {
  const response = await fetch(`http://localhost:8000/api/assignment/${assignmentId}/file/${fileId}`, {
    method: "GET"
  });

  if (!response.ok) {
    throw new Error("Error al descargar el archivo");
  }

  return response.blob();
}