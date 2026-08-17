import api from './client';
import type { ChatResponse } from '../types';

interface SymptomCheckRequest {
  main_symptom: string;
  duration: string;
  severity: string;
  age_group: string;
  existing_conditions: string;
  medications: string;
  other_symptoms: string;
  triggers: string;
}

export const symptomsAPI = {
  check: async (data: SymptomCheckRequest): Promise<ChatResponse> => {
    const res = await api.post('/symptoms/check/', data);
    return res.data;
  },
};
