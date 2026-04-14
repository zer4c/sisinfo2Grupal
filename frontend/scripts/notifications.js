import { getNotificationsByStudent } from "./api/studentApi.js";
import { getAssignmentsBySubject } from "./api/assignmentApi.js";
import { getSubjectsByStudent } from "./api/subjectApi.js";

let notificationCache = {};

async function getAssignmentById(assignmentId) {
  if (notificationCache[`assignment_${assignmentId}`]) {
    return notificationCache[`assignment_${assignmentId}`];
  }

  try {
    const response = await fetch(`http://localhost:8000/api/assignment/${assignmentId}`);
    if (!response.ok) throw new Error("Error al obtener tarea");
    
    const data = await response.json();
    notificationCache[`assignment_${assignmentId}`] = data.data;
    return data.data;
  } catch (err) {
    console.error("Error obteniendo asignación:", err);
    return null;
  }
}

async function getSubmissionById(submissionId) {
  if (notificationCache[`submission_${submissionId}`]) {
    return notificationCache[`submission_${submissionId}`];
  }

  try {
    const response = await fetch(`http://localhost:8000/api/submission/details/${submissionId}`);
    if (!response.ok) throw new Error("Error al obtener entrega");
    
    const data = await response.json();
    notificationCache[`submission_${submissionId}`] = data.data;
    return data.data;
  } catch (err) {
    console.error("Error obteniendo submission:", err);
    return null;
  }
}

export async function loadNotifications(studentId) {
  try {
    const notificationsResponse = await getNotificationsByStudent(studentId);
    const notifications = notificationsResponse.data || [];

    if (!notifications.length) {
      renderEmptyNotifications();
      return;
    }

    const notificationsWithDetails = await Promise.all(
      notifications.map(async (notification) => {
        const submission = await getSubmissionById(notification.submission_id);
        if (!submission) return null;

        const assignment = await getAssignmentById(submission.assignment_id);
        if (!assignment) return null;

        return {
          id: notification.id,
          submission_id: notification.submission_id,
          comment_id: notification.comment_id,
          task_name: assignment.title || "Sin título",
          created_at: new Date()
        };
      })
    );

    const validNotifications = notificationsWithDetails.filter(n => n !== null);

    if (validNotifications.length === 0) {
      renderEmptyNotifications();
      return;
    }

    renderNotifications(validNotifications);
    showNotificationsSidebar();
  } catch (err) {
    console.error("Error al cargar notificaciones:", err);
    renderEmptyNotifications();
  }
}

function renderNotifications(notifications) {
  const notificationsList = document.getElementById("notifications-list");
  
  notificationsList.innerHTML = notifications
    .map(notification => `
      <div class="notification-item">
        <div class="notification-item-title">Nuevo comentario</div>
        <div class="notification-item-subtitle">${notification.task_name}</div>
        <div class="notification-item-date">Hace poco</div>
      </div>
    `)
    .join("");
}

function renderEmptyNotifications() {
  const notificationsList = document.getElementById("notifications-list");
  notificationsList.innerHTML = '<div class="notifications-empty">Sin notificaciones</div>';
}

function showNotificationsSidebar() {
  const sidebar = document.getElementById("notifications-sidebar");
  
  if (sidebar) sidebar.style.display = "flex";
}

export function hideNotificationsSidebar() {
  const sidebar = document.getElementById("notifications-sidebar");
  
  if (sidebar) sidebar.style.display = "none";
}
