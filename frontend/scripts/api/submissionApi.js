export async function getSubmissionByStudent(studentId, assignmentId) {
    const response = await fetch(`http://localhost:8000/api/submission/student/${studentId}/assignment/${assignmentId}/`);
    if (!response.ok) throw { status: response.status };
    return response.json();
}