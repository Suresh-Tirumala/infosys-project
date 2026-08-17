import api from './client';
import type { HealthProfile } from '../types';

export const healthProfileAPI = {
  get: async (): Promise<HealthProfile> => {
    const res = await api.get('/health-profile/');
    return res.data;
  },

  update: async (data: Partial<HealthProfile>): Promise<HealthProfile> => {
    const res = await api.put('/health-profile/', data);
    return res.data;
  },

  delete: async () => {
    const res = await api.delete('/health-profile/');
    return res.data;
  },
};
