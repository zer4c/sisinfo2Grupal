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
  const response = await fetch(`http://localhost:8000/api/subject/teacher?teacher_id=${teacher_id}`);
  if (!response.ok) throw new Error("Error fetching subjects");
  return await response.json();
}

export async function getSubjectsByStudent(student_id) {
  const response = await fetch(`http://localhost:8000/api/subject/student?id_student=${student_id}`);
  if (!response.ok) throw new Error("Error fetching subjects");
  return await response.json();
}

export async function enrollStudent(id_subject, id_student) {
  const response = await fetch("http://localhost:8000/api/subject/enrollment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_subject, id_student })
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Error al unirse a la clase");
  }
  return await response.json();
}