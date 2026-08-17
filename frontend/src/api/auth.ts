import api from './client';
import type { Token, User } from '../types';

export const authAPI = {
  register: async (data: {
    username: string;
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }): Promise<Token> => {
    const res = await api.post('/auth/register/', data);
    return res.data;
  },

  login: async (email: string, password: string): Promise<Token> => {
    const res = await api.post('/auth/login/', { email, password });
    return res.data;
  },

  getMe: async (): Promise<User> => {
    const res = await api.get('/auth/me/');
    return res.data;
  },

  deleteAccount: async () => {
    const res = await api.delete('/auth/me/');
    return res.data;
  },
};
