import React, { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import api from '../api/client';

const SettingsPage: React.FC = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [settings, setSettings] = useState({
    language: 'en',
    voice_enabled: false,
    notification_enabled: true,
    data_retention_days: 90,
    share_analytics: false,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const res = await api.get('/settings');
      setSettings(res.data);
    } catch (err: any) {
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');
    try {
      await api.put('/settings', settings);
      setMessage('Settings saved successfully');
    } catch (err: any) {
      setMessage('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteConversations = async () => {
    if (!confirm('Delete all your conversations? This cannot be undone.')) return;
    try {
      await api.delete('/settings/conversations');
      setMessage('All conversations deleted');
    } catch (err: any) {
      setMessage('Failed to delete conversations');
    }
  };

  const handleDeleteAllData = async () => {
    if (!confirm('Delete ALL your data including conversations, documents, and reports? This cannot be undone.')) return;
    try {
      await api.delete('/settings/data');
      setMessage('All data deleted');
    } catch (err: any) {
      setMessage('Failed to delete data');
    }
  };

  const handleDeleteAccount = async () => {
    if (!confirm('Delete your account? This action is permanent and cannot be undone.')) return;
    try {
      await api.delete('/auth/me');
      logout();
    } catch (err: any) {
      setMessage('Failed to delete account');
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Settings</h1>

        {message && (
          <div className={`mb-4 px-4 py-3 rounded-lg text-sm ${
            message.includes('success') || message.includes('deleted')
              ? 'bg-green-50 border border-green-200 text-green-700'
              : 'bg-red-50 border border-red-200 text-red-700'
          }`}>
            {message}
          </div>
        )}

        <div className="space-y-6">
          {/* Appearance */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Appearance</h2>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Dark Mode</p>
                <p className="text-sm text-gray-500">Toggle between light and dark themes</p>
              </div>
              <button
                onClick={toggleTheme}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  theme === 'dark' ? 'bg-primary-600' : 'bg-gray-300'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  theme === 'dark' ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </div>
          </div>

          {/* Preferences */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
                <select
                  value={settings.language}
                  onChange={(e) => setSettings(prev => ({ ...prev, language: e.target.value }))}
                  className="input-field"
                >
                  <option value="en">English</option>
                  <option value="hi" disabled>हिन्दी (Coming Soon)</option>
                  <option value="ta" disabled>தமிழ் (Coming Soon)</option>
                  <option value="te" disabled>తెలుగు (Coming Soon)</option>
                  <option value="bn" disabled>বাংলা (Coming Soon)</option>
                </select>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Voice Input</p>
                  <p className="text-sm text-gray-500">Enable voice input for describing symptoms</p>
                </div>
                <button
                  onClick={() => setSettings(prev => ({ ...prev, voice_enabled: !prev.voice_enabled }))}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.voice_enabled ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.voice_enabled ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
            </div>
          </div>

          {/* Privacy */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Privacy & Data</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Notifications</p>
                  <p className="text-sm text-gray-500">Receive health tips and reminders</p>
                </div>
                <button
                  onClick={() => setSettings(prev => ({ ...prev, notification_enabled: !prev.notification_enabled }))}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.notification_enabled ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.notification_enabled ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Share Anonymous Analytics</p>
                  <p className="text-sm text-gray-500">Help improve the service</p>
                </div>
                <button
                  onClick={() => setSettings(prev => ({ ...prev, share_analytics: !prev.share_analytics }))}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.share_analytics ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.share_analytics ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
              <div className="pt-4 border-t border-gray-200 space-y-3">
                <button onClick={handleDeleteConversations} className="text-sm text-red-600 hover:text-red-700 font-medium">
                  Delete All Conversations
                </button>
                <button onClick={handleDeleteAllData} className="block text-sm text-red-600 hover:text-red-700 font-medium">
                  Delete All Data
                </button>
                <button onClick={handleDeleteAccount} className="block text-sm text-red-600 hover:text-red-700 font-medium">
                  Delete Account
                </button>
              </div>
            </div>
          </div>

          <button onClick={handleSave} disabled={saving} className="btn-primary px-6">
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>
    </Layout>
  );
};

export default SettingsPage;
