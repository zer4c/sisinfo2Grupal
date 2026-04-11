export async function createSubject(data) {
  const response = await fetch("http://localhost:8000/api/subject/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error("Error creating subject");
  }

  return await response.json();
}

export async function getSubjectsByTeacher(teacher_id) {
  const response = await fetch(`http://localhost:8000/api/subject/?teacher_id=${teacher_id}`);
  if (!response.ok) throw new Error("Error fetching subjects");
  return await response.json();
}