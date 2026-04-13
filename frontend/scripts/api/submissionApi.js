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
