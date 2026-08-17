import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useConversations } from '../../hooks/useConversations';

interface ConversationSidebarProps {
  currentConversationId: number | null;
  onSelectConversation: (id: number) => void;
  isOpen: boolean;
  onClose: () => void;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  currentConversationId,
  onSelectConversation,
  isOpen,
  onClose,
}) => {
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

  return (
    <>
      {isOpen && <div className="fixed inset-0 bg-black/20 z-30 lg:hidden" onClick={onClose} />}
      <div
        className={`fixed lg:static inset-y-0 left-0 z-40 w-72 bg-white border-r border-gray-200
                    transform transition-transform duration-200 ease-in-out
                    ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-gray-900">Conversations</h2>
              <button
                onClick={() => { navigate('/chat'); onClose(); }}
                className="text-xs text-primary-600 hover:text-primary-700 font-medium"
              >
                + New
              </button>
            </div>
            <input
              type="text"
              placeholder="Search conversations..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg
                         focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="p-4 text-center text-sm text-gray-500">Loading...</div>
            ) : filtered.length === 0 ? (
              <div className="p-4 text-center text-sm text-gray-500">No conversations found</div>
            ) : (
              filtered.map((conv) => (
                <div
                  key={conv.id}
                  className={`px-4 py-3 border-b border-gray-100 cursor-pointer hover:bg-gray-50
                             ${currentConversationId === conv.id ? 'bg-primary-50 border-l-2 border-l-primary-600' : ''}`}
                  onClick={() => { onSelectConversation(conv.id); onClose(); }}
                >
                  {editingId === conv.id ? (
                    <input
                      autoFocus
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      onBlur={() => handleRename(conv.id)}
                      onKeyDown={(e) => e.key === 'Enter' && handleRename(conv.id)}
                      className="w-full text-sm border border-primary-300 rounded px-2 py-1 focus:outline-none"
                      onClick={(e) => e.stopPropagation()}
                    />
                  ) : (
                    <>
                      <p className="text-sm font-medium text-gray-900 truncate">{conv.title}</p>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-xs text-gray-500">
                          {new Date(conv.updated_at).toLocaleDateString()}
                        </span>
                        <div className="flex gap-1">
                          <button
                            onClick={(e) => { e.stopPropagation(); setEditingId(conv.id); setEditTitle(conv.title); }}
                            className="text-xs text-gray-400 hover:text-gray-600"
                          >
                            Edit
                          </button>
                          <button
                            onClick={(e) => { e.stopPropagation(); deleteConversation(conv.id); }}
                            className="text-xs text-red-400 hover:text-red-600"
                          >
                            Del
                          </button>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default ConversationSidebar;
