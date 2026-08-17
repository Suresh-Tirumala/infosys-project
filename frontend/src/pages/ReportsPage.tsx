import React from 'react';
import Layout from '../components/layout/Layout';
import DocumentUpload from '../components/documents/DocumentUpload';

const ReportsPage: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Health Documents</h1>
        <p className="text-gray-600 mb-6">
          Upload health documents for AI-powered explanations and summaries.
        </p>
        <div className="card p-6">
          <DocumentUpload />
        </div>
        <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-amber-800">
          <strong>Note:</strong> Document analysis is for informational purposes only.
          Always have your healthcare professional interpret medical reports.
        </div>
      </div>
    </Layout>
  );
};

export default ReportsPage;
