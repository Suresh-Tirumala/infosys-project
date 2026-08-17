import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import RegisterForm from '../components/auth/RegisterForm';

const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const [error, setError] = useState('');

  const handleRegister = async (data: { username: string; email: string; password: string; first_name: string; last_name: string }) => {
    setError('');
    try {
      await register(data);
    } catch (err: any) {
      const data = err.response?.data;
      let msg = 'Registration failed. Please try again.';
      if (data?.detail && typeof data.detail === 'string') {
        msg = data.detail;
      } else if (data) {
        const messages = Object.entries(data)
          .filter(([key]) => key !== 'non_field_errors')
          .flatMap(([, errors]) => (Array.isArray(errors) ? errors : [String(errors)]));
        if (messages.length > 0) {
          msg = messages.join(', ');
        }
      }
      setError(msg);
    }
  };

  return <RegisterForm onSubmit={handleRegister} error={error} />;
};

export default RegisterPage;
