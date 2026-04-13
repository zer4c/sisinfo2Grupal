import { getSubmissionByStudent } from './api/submissionApi.js';

export const STATE_LABELS = {
    1: { label: 'Nuevo', class: 'state-nuevo' },
    2: { label: 'Entregado', class: 'state-entregado' },
    3: { label: 'Revisado', class: 'state-revisado' },
};

export async function getAssignmentState(userId, assignmentId) {
    if (!userId || !assignmentId) {
        return STATE_LABELS[1];
    }
    
    try {
        const res = await getSubmissionByStudent(userId, assignmentId);
        let stateId = 1;
        
        if (res && res.data) {
            stateId = res.data.state_id || 1;
        } else if (res && res.state_id) {
            stateId = res.state_id;
        }
        
        return STATE_LABELS[stateId] || STATE_LABELS[1];
    } catch (error) {
        return STATE_LABELS[1];
    }
}

export function createStateBadge(state) {
    if (!state || !state.class || !state.label) {
        return `<span class="assignment-state state-nuevo">Nuevo</span>`;
    }
    return `<span class="assignment-state ${state.class}">${state.label}</span>`;
}