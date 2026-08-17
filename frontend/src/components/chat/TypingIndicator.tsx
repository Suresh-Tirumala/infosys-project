import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex justify-start mb-4 animate-fade-in">
      <div className="flex items-center gap-2 mb-1">
        <div className="w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
          <svg className="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </div>
        <span className="text-xs font-medium text-gray-500">HealthChat AI is thinking...</span>
      </div>
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 ml-8 border-l-4 border-l-primary-500">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 bg-primary-400 rounded-full typing-dot"></div>
          <div className="w-2 h-2 bg-primary-400 rounded-full typing-dot"></div>
          <div className="w-2 h-2 bg-primary-400 rounded-full typing-dot"></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
