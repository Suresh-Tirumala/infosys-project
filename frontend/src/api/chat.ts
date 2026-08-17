import api from './client';
import type { ChatResponse } from '../types';

export const chatAPI = {
  sendMessage: async (
    message: string,
    conversationId?: number,
    language: string = 'en'
  ): Promise<ChatResponse> => {
    const res = await api.post('/chat/', {
      message,
      conversation_id: conversationId,
      language,
    });
    return res.data;
  },
};
