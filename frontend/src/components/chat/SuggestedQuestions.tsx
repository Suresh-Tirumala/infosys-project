import React from 'react';

interface SuggestedQuestionsProps {
  onQuestionClick: (question: string) => void;
}

const questions = [
  "I have a headache that won't go away",
  "What should I do about a persistent cough?",
  "I've been feeling tired lately",
  "What are common causes of back pain?",
  "I have a mild fever, should I be worried?",
  "How can I improve my sleep quality?",
];

const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({ onQuestionClick }) => {
  return (
    <div className="px-4 py-6">
      <div className="max-w-2xl mx-auto">
        <h3 className="text-sm font-medium text-gray-500 mb-3">Suggested questions:</h3>
        <div className="flex flex-wrap gap-2">
          {questions.map((q, i) => (
            <button
              key={i}
              onClick={() => onQuestionClick(q)}
              className="px-3 py-2 text-sm text-gray-700 bg-white border border-gray-200 rounded-lg
                         hover:bg-primary-50 hover:border-primary-300 hover:text-primary-700
                         transition-all duration-200"
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SuggestedQuestions;
