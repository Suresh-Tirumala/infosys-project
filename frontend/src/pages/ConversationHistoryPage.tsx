import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import { useConversations } from '../hooks/useConversations';

const ConversationHistoryPage: React.FC = () => {
  const { conversations, loading, deleteConversation, renameConversation } = useConversations();
  const [search, setSearch] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const navigate = useNavigate();

  const filtered = conversations.filter(c =>
    c.title.toLowerCase().includes(search.toLowerCase())
  );

  const handleRename = async (id: number) => {
    if (editTitle.trim()) {
      await renameConversation(id, editTitle.trim());
    }
    setEditingId(null);
  };

  const riskBadge = (level: string) => {
    switch (level) {
      case 'moderate': return <span className="badge-yellow">Moderate</span>;
      case 'high': return <span className="badge-red">High</span>;
      case 'emergency': return <span className="badge-red bg-red-200">Emergency</span>;
      default: return <span className="badge-green">Low</span>;
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Conversation History</h1>
            <p className="text-gray-600 mt-1">View and manage your past health conversations</p>
          </div>
          <button onClick={() => navigate('/chat')} className="btn-primary">
            New Conversation
          </button>
        </div>

        <div className="mb-4">
          <input
            type="text"
            placeholder="Search conversations..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field"
          />
        </div>

        {loading ? (
          <div className="text-center py-12 text-gray-500">Loading conversations...</div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">No conversations found</p>
            <button onClick={() => navigate('/chat')} className="btn-primary">
              Start a Conversation
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((conv) => (
              <div
                key={conv.id}
                className="card p-4 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => navigate(`/chat/${conv.id}`)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    {editingId === conv.id ? (
                      <input
                        autoFocus
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        onBlur={() => handleRename(conv.id)}
                        onKeyDown={(e) => e.key === 'Enter' && handleRename(conv.id)}
                        className="input-field text-sm"
                        onClick={(e) => e.stopPropagation()}
                      />
                    ) : (
                      <h3 className="font-medium text-gray-900 truncate">{conv.title}</h3>
                    )}
                    <div className="flex items-center gap-3 mt-1">
                      <span className="text-xs text-gray-500">
                        {new Date(conv.updated_at).toLocaleString()}
                      </span>
                      <span className="text-xs text-gray-500 capitalize">{conv.category}</span>
                      {riskBadge(conv.risk_level)}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <button
                      onClick={(e) => { e.stopPropagation(); setEditingId(conv.id); setEditTitle(conv.title); }}
                      className="text-gray-400 hover:text-gray-600 p-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); if (confirm('Delete this conversation?')) deleteConversation(conv.id); }}
                      className="text-gray-400 hover:text-red-600 p-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ConversationHistoryPage;
