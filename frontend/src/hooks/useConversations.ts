import { useState, useEffect, useCallback } from 'react';
import { conversationsAPI } from '../api/conversations';
import type { Conversation } from '../types';

export const useConversations = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadConversations = useCallback(async (search?: string) => {
    setLoading(true);
    try {
      const data = await conversationsAPI.list(search);
      setConversations(data);
    } catch (err) {
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const deleteConversation = async (id: number) => {
    try {
      await conversationsAPI.delete(id);
      setConversations(prev => prev.filter(c => c.id !== id));
    } catch (err) {
      setError('Failed to delete conversation');
    }
  };

  const renameConversation = async (id: number, title: string) => {
    try {
      await conversationsAPI.update(id, title);
      setConversations(prev =>
        prev.map(c => (c.id === id ? { ...c, title } : c))
      );
    } catch (err) {
      setError('Failed to rename conversation');
    }
  };

  return {
    conversations,
    loading,
    error,
    loadConversations,
    deleteConversation,
    renameConversation,
  };
};
