import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import LoginForm from '../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const [error, setError] = useState('');

  const handleLogin = async (email: string, password: string) => {
    setError('');
    try {
      await login(email, password);
    } catch (err: any) {
      const data = err.response?.data;
      let msg = 'Invalid email or password';
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

  return <LoginForm onSubmit={handleLogin} error={error} />;
};

export default LoginPage;
