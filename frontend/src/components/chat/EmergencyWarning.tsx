import React from 'react';

interface EmergencyWarningProps {
  isVisible: boolean;
  message?: string;
  onClose?: () => void;
}

const EmergencyWarning: React.FC<EmergencyWarningProps> = ({ isVisible, message, onClose }) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl p-8 max-w-lg mx-4 shadow-2xl border-2 border-red-500 animate-fade-in">
        <div className="flex items-center justify-center mb-4">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center animate-pulse">
            <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
        </div>
        <h2 className="text-2xl font-bold text-red-600 text-center mb-3">
          MEDICAL EMERGENCY DETECTED
        </h2>
        <p className="text-gray-700 text-center mb-4">
          {message || "Based on your description, you may be experiencing a medical emergency."}
        </p>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-red-800 mb-2">IMMEDIATE ACTIONS:</h3>
          <ol className="list-decimal list-inside text-sm text-red-700 space-y-1">
            <li>Call emergency services immediately (911 / 112 / 999)</li>
            <li>Go to the nearest emergency room</li>
            <li>Do not drive yourself - call for help</li>
          </ol>
        </div>
        <div className="text-center">
          <a
            href="tel:911"
            className="inline-flex items-center gap-2 bg-red-600 text-white px-6 py-3 rounded-xl font-semibold
                       hover:bg-red-700 transition-colors text-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            Call Emergency Services
          </a>
          {onClose && (
            <button
              onClick={onClose}
              className="block mx-auto mt-3 text-sm text-gray-500 hover:text-gray-700"
            >
              I understand, dismiss
            </button>
          )}
        </div>
        <p className="text-xs text-gray-400 text-center mt-4">
          This AI cannot provide emergency care. Always seek professional medical help.
        </p>
      </div>
    </div>
  );
};

export default EmergencyWarning;
