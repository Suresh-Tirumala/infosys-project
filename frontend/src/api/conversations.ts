import api from './client';
import type { Conversation, Message } from '../types';

export const conversationsAPI = {
  list: async (search?: string): Promise<Conversation[]> => {
    const params = search ? { search } : {};
    const res = await api.get('/conversations/', { params });
    return res.data;
  },

  create: async (title: string, category: string = 'general'): Promise<Conversation> => {
    const res = await api.post('/conversations/', { title, category });
    return res.data;
  },

  get: async (id: number): Promise<Conversation> => {
    const res = await api.get(`/conversations/${id}/`);
    return res.data;
  },

  update: async (id: number, title: string) => {
    const res = await api.put(`/conversations/${id}/`, null, { params: { title } });
    return res.data;
  },

  delete: async (id: number) => {
    const res = await api.delete(`/conversations/${id}/`);
    return res.data;
  },

  getMessages: async (id: number): Promise<Message[]> => {
    const res = await api.get(`/conversations/${id}/messages/`);
    return res.data;
  },
};
