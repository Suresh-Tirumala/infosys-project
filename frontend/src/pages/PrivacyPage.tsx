import React from 'react';
import Layout from '../components/layout/Layout';

const PrivacyPage: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Privacy & Safety</h1>

        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Data Collection</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <p>We collect only the information necessary to provide our service:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Account information (email, username)</li>
                <li>Health profile (optional)</li>
                <li>Conversation history</li>
                <li>Uploaded documents</li>
              </ul>
              <p>We do NOT collect unnecessary personal information.</p>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Data Usage</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <p>Your data is used solely to:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Provide health information and guidance</li>
                <li>Maintain your conversation history</li>
                <li>Personalize responses based on your health profile</li>
              </ul>
              <p className="font-medium mt-3">We NEVER sell or share your health information with third parties.</p>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Security Measures</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <ul className="list-disc list-inside space-y-1">
                <li>Password hashing with bcrypt</li>
                <li>Secure JWT authentication</li>
                <li>HTTPS encryption in production</li>
                <li>Input validation and sanitization</li>
                <li>Rate limiting to prevent abuse</li>
                <li>API key protection (never exposed to frontend)</li>
              </ul>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Your Rights</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <ul className="list-disc list-inside space-y-1">
                <li>Access your data anytime</li>
                <li>Delete individual conversations</li>
                <li>Delete all your data</li>
                <li>Delete your account</li>
                <li>Control notification preferences</li>
                <li>Control analytics sharing</li>
              </ul>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">AI Safety</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <ul className="list-disc list-inside space-y-1">
                <li>AI never claims to provide diagnoses</li>
                <li>Emergency detection system for dangerous symptoms</li>
                <li>Safety layer prevents dangerous advice</li>
                <li>Always recommends professional medical consultation</li>
                <li>Uses simple, clear language</li>
                <li>Communicates uncertainty honestly</li>
              </ul>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Data Retention</h2>
            <div className="text-sm text-gray-700 space-y-2">
              <p>Your data is retained until you choose to delete it. You can:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Delete specific conversations from the History page</li>
                <li>Delete all data from Settings</li>
                <li>Deactivate your account (Account settings)</li>
              </ul>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-800">
            <strong>Important:</strong> This application does not claim to be HIPAA or GDPR compliant.
            Compliance requires specific infrastructure and legal requirements that must be
            independently verified and certified.
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default PrivacyPage;
