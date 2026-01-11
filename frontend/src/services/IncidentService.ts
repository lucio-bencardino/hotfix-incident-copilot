import { api } from 'boot/axios';

export interface IncidentPayload {
    description: string;
    logs: string;
    context: string;
    role: string | null;
}

export interface IncidentPlan {
    steps: string[];
    warnings: string[];
}

export interface HealthResponse {
    status: string;
    version: string;
    service: string;
}

export const IncidentService = {
    async checkHealth(): Promise<HealthResponse> {
        const response = await api.get('/health');
        return response.data;
    },

    async generatePlan(payload: IncidentPayload): Promise<IncidentPlan> {
        const response = await api.post('/generate-plan', payload);
        return response.data;
    },
};
