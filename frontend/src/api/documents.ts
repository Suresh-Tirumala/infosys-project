import api from './client';
import type { UploadedDocument, ChatResponse } from '../types';

export const documentsAPI = {
  upload: async (file: File): Promise<UploadedDocument> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post('/documents/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  list: async (): Promise<UploadedDocument[]> => {
    const res = await api.get('/documents/');
    return res.data;
  },

  get: async (id: number): Promise<UploadedDocument> => {
    const res = await api.get(`/documents/${id}/`);
    return res.data;
  },

  delete: async (id: number) => {
    const res = await api.delete(`/documents/${id}/`);
    return res.data;
  },

  askAboutDocument: async (docId: number, question: string): Promise<{ response: string }> => {
    const res = await api.post(`/documents/${docId}/ask/`, null, {
      params: { question },
    });
    return res.data;
  },
};
