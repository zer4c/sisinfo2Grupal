export async function createAssignment(data) {
  const response = await fetch("http://localhost:8000/api/assignment/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al crear la tarea");
  }

  return await response.json();
}