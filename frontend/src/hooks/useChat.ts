import { useState, useCallback, useRef } from 'react';
import { chatAPI } from '../api/chat';
import type { Message, ChatResponse } from '../types';

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    setLoading(true);
    setError(null);

    const userMessage: Message = {
      id: Date.now(),
      conversation_id: conversationId || 0,
      role: 'user',
      content,
      risk_level: 'low',
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await chatAPI.sendMessage(content, conversationId || undefined);

      const botMessage: Message = {
        id: Date.now() + 1,
        conversation_id: response.conversation_id,
        role: 'assistant',
        content: response.reply,
        risk_level: response.risk_level,
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, botMessage]);
      setConversationId(response.conversation_id);
      setLastResponse(response);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to get response. Please try again.';
      setError(errorMessage);
      setMessages(prev => prev.filter(m => m.id !== userMessage.id));
    } finally {
      setLoading(false);
    }
  }, [conversationId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setLastResponse(null);
    setError(null);
  }, []);

  const loadConversation = useCallback(async (id: number) => {
    setLoading(true);
    try {
      const { conversationsAPI } = await import('../api/conversations');
      const msgs = await conversationsAPI.getMessages(id);
      setMessages(msgs);
      setConversationId(id);
    } catch (err) {
      setError('Failed to load conversation');
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    messages,
    loading,
    conversationId,
    error,
    lastResponse,
    sendMessage,
    clearMessages,
    loadConversation,
  };
};
