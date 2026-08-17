import React, { useState, useEffect, useRef } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import MessageBubble from '../components/chat/MessageBubble';
import TypingIndicator from '../components/chat/TypingIndicator';
import ChatInput from '../components/chat/ChatInput';
import EmergencyWarning from '../components/chat/EmergencyWarning';
import SuggestedQuestions from '../components/chat/SuggestedQuestions';
import ConversationSidebar from '../components/chat/ConversationSidebar';
import { useChat } from '../hooks/useChat';

const ChatPage: React.FC = () => {
  const { conversationId } = useParams();
  const [searchParams] = useSearchParams();
  const { messages, loading, conversationId: currentConvId, error, lastResponse, sendMessage, clearMessages, loadConversation } = useChat();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showEmergency, setShowEmergency] = useState(false);
  const [emergencyMessage, setEmergencyMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (conversationId) {
      loadConversation(parseInt(conversationId));
    }
  }, [conversationId, loadConversation]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    if (lastResponse?.is_emergency) {
      setEmergencyMessage(lastResponse.reply);
      setShowEmergency(true);
    }
  }, [lastResponse]);

  const handleSend = async (message: string) => {
    await sendMessage(message);
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const category = searchParams.get('category');
  const topic = searchParams.get('topic');

  return (
    <Layout showNavbar={false}>
      <div className="flex h-screen">
        <ConversationSidebar
          currentConversationId={currentConvId}
          onSelectConversation={(id) => loadConversation(id)}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-sm font-semibold text-gray-900">HealthChat AI</h1>
                <p className="text-xs text-gray-500">General health information assistant</p>
              </div>
            </div>
            <div className="ml-auto flex items-center gap-2">
              <button
                onClick={clearMessages}
                className="text-xs text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-100"
              >
                New Chat
              </button>
            </div>
          </div>

          {/* Risk Level Banner */}
          {lastResponse && lastResponse.risk_level !== 'low' && !lastResponse.is_emergency && (
            <div className={`px-4 py-2 text-sm text-center ${
              lastResponse.risk_level === 'moderate' ? 'bg-yellow-50 text-yellow-800 border-b border-yellow-200' :
              lastResponse.risk_level === 'high' ? 'bg-orange-50 text-orange-800 border-b border-orange-200' :
              'bg-red-50 text-red-800 border-b border-red-200'
            }`}>
              {lastResponse.risk_level === 'moderate' && 'Monitor your symptoms. Consider consulting a healthcare professional.'}
              {lastResponse.risk_level === 'high' && 'Please consider contacting a healthcare professional promptly.'}
            </div>
          )}

          {/* Safety Warnings */}
          {lastResponse && lastResponse.safety_warnings.length > 0 && (
            <div className="bg-amber-50 border-b border-amber-200 px-4 py-2">
              {lastResponse.safety_warnings.map((w, i) => (
                <p key={i} className="text-xs text-amber-800">Warning: {w}</p>
              ))}
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-6">
            {messages.length === 0 && !loading ? (
              <div className="text-center py-12">
                <div className="w-16 h-12 bg-primary-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  {topic ? `Discussing: ${topic}` : 'HealthChat AI'}
                </h2>
                <p className="text-gray-600 mb-6 max-w-md mx-auto">
                  I can help with general health questions and symptom guidance.
                  Remember, I provide information, not diagnoses.
                </p>
                <SuggestedQuestions onQuestionClick={handleSend} />
              </div>
            ) : (
              <div className="max-w-3xl mx-auto">
                {messages.map((msg) => (
                  <MessageBubble key={msg.id} message={msg} onCopy={handleCopy} />
                ))}
                {loading && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Follow-up Questions */}
          {lastResponse && lastResponse.follow_up_questions.length > 0 && !loading && (
            <div className="px-4 py-2 border-t border-gray-100">
              <div className="max-w-3xl mx-auto flex flex-wrap gap-2">
                {lastResponse.follow_up_questions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(q)}
                    className="text-xs px-3 py-1.5 bg-primary-50 text-primary-700 rounded-full
                               hover:bg-primary-100 transition-colors border border-primary-200"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <ChatInput
            onSend={handleSend}
            disabled={loading}
          />
        </div>
      </div>

      <EmergencyWarning
        isVisible={showEmergency}
        message={emergencyMessage}
        onClose={() => setShowEmergency(false)}
      />
    </Layout>
  );
};

export default ChatPage;
