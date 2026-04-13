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
  formData.append('assignment_id', assignment_id);
  formData.append('type_file', ext);
  formData.append('data', file, file.name);

  for (let [key, value] of formData.entries()) {
    console.log(key, value);
  }
  const response = await fetch(`http://localhost:8000/api/assignment/${assignment_id}/file`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al subir el archivo");
  }

  return await response.json();
}