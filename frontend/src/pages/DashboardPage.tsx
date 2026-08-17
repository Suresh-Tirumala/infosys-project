import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import HealthCategories from '../components/health/HealthCategories';
import { useAuth } from '../context/AuthContext';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">
            Welcome back, {user?.first_name || user?.username}
          </h1>
          <p className="text-gray-600 mt-1">
            How can we help you today?
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Link
            to="/chat"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary-200 transition-colors">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Start Chat</h3>
            <p className="text-sm text-gray-600">Describe symptoms or ask health questions</p>
          </Link>

          <Link
            to="/symptom-checker"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-orange-200 transition-colors">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Symptom Checker</h3>
            <p className="text-sm text-gray-600">Structured symptom analysis</p>
          </Link>

          <Link
            to="/reports"
            className="card p-6 hover:shadow-md transition-shadow group"
          >
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Documents</h3>
            <p className="text-sm text-gray-600">Upload and analyze health documents</p>
          </Link>
        </div>

        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Health Categories</h2>
          <HealthCategories />
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-8">
          <p className="text-sm text-amber-800">
            <strong>Disclaimer:</strong> HealthChat AI provides general health information only.
            It is not a substitute for professional medical advice, diagnosis, or treatment.
            Always seek the advice of your physician or other qualified health provider.
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
