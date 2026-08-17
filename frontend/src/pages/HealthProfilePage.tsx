import React from 'react';
import Layout from '../components/layout/Layout';
import HealthProfileComponent from '../components/health/HealthProfile';

const HealthProfilePage: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Health Profile</h1>
        <p className="text-gray-600 mb-6">
          Optional health information to help provide more relevant guidance.
        </p>
        <div className="card p-6">
          <HealthProfileComponent />
        </div>
      </div>
    </Layout>
  );
};

export default HealthProfilePage;
