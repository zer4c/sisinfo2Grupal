export async function getStudentById(studentId) {
  const response = await fetch(`http://localhost:8000/api/student/${studentId}`);

  if (!response.ok) {
    throw new Error("Error al obtener información del estudiante");
  }

  return await response.json();
}
