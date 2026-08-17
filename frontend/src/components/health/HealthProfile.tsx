import React, { useState, useEffect } from 'react';
import { healthProfileAPI } from '../../api/healthProfile';
import type { HealthProfile } from '../../types';

const HealthProfileComponent: React.FC = () => {
  const [profile, setProfile] = useState<HealthProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await healthProfileAPI.get();
      setProfile(data);
    } catch (err: any) {
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    setMessage('');
    try {
      const updated = await healthProfileAPI.update({
        age: profile.age,
        sex: profile.sex,
        height: profile.height,
        weight: profile.weight,
        blood_type: profile.blood_type,
        allergies: profile.allergies,
        existing_conditions: profile.existing_conditions,
        current_medications: profile.current_medications,
        emergency_contact: profile.emergency_contact,
      });
      setProfile(updated);
      setMessage('Profile updated successfully');
    } catch (err: any) {
      setMessage('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field: keyof HealthProfile, value: any) => {
    if (!profile) return;
    setProfile({ ...profile, [field]: value });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!profile) return null;

  return (
    <div className="space-y-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
        <p><strong>Privacy Note:</strong> Your health profile helps provide more relevant health information.
        All data is stored securely and is never shared with third parties. You can delete your data at any time.</p>
      </div>

      {message && (
        <div className={`px-4 py-3 rounded-lg text-sm ${
          message.includes('success') ? 'bg-green-50 border border-green-200 text-green-700'
            : 'bg-red-50 border border-red-200 text-red-700'
        }`}>
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
          <input
            type="number"
            value={profile.age || ''}
            onChange={(e) => handleChange('age', e.target.value ? parseInt(e.target.value) : null)}
            className="input-field"
            placeholder="Enter your age"
            min={0}
            max={150}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Sex</label>
          <select
            value={profile.sex || ''}
            onChange={(e) => handleChange('sex', e.target.value || null)}
            className="input-field"
          >
            <option value="">Select</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer-not-to-say">Prefer not to say</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Height (cm)</label>
          <input
            type="number"
            value={profile.height || ''}
            onChange={(e) => handleChange('height', e.target.value ? parseFloat(e.target.value) : null)}
            className="input-field"
            placeholder="Height in cm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Weight (kg)</label>
          <input
            type="number"
            value={profile.weight || ''}
            onChange={(e) => handleChange('weight', e.target.value ? parseFloat(e.target.value) : null)}
            className="input-field"
            placeholder="Weight in kg"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Blood Type</label>
          <select
            value={profile.blood_type || ''}
            onChange={(e) => handleChange('blood_type', e.target.value || null)}
            className="input-field"
          >
            <option value="">Select</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Emergency Contact</label>
          <input
            type="text"
            value={profile.emergency_contact}
            onChange={(e) => handleChange('emergency_contact', e.target.value)}
            className="input-field"
            placeholder="Name & phone number"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Known Allergies</label>
        <textarea
          value={profile.allergies}
          onChange={(e) => handleChange('allergies', e.target.value)}
          className="input-field"
          rows={3}
          placeholder="List any known allergies (optional)"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Existing Medical Conditions</label>
        <textarea
          value={profile.existing_conditions}
          onChange={(e) => handleChange('existing_conditions', e.target.value)}
          className="input-field"
          rows={3}
          placeholder="List any existing conditions (optional)"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Current Medications</label>
        <textarea
          value={profile.current_medications}
          onChange={(e) => handleChange('current_medications', e.target.value)}
          className="input-field"
          rows={3}
          placeholder="List current medications (optional)"
        />
      </div>

      <div className="flex justify-end">
        <button onClick={handleSave} disabled={saving} className="btn-primary px-6">
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </div>
    </div>
  );
};

export default HealthProfileComponent;
