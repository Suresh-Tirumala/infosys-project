import React, { useState } from 'react';
import Layout from '../components/layout/Layout';
import { symptomsAPI } from '../api/symptoms';
import EmergencyWarning from '../components/chat/EmergencyWarning';
import ReactMarkdown from 'react-markdown';

const SymptomCheckerPage: React.FC = () => {
  const [formData, setFormData] = useState({
    main_symptom: '',
    duration: '',
    severity: '',
    age_group: '',
    existing_conditions: '',
    medications: '',
    other_symptoms: '',
    triggers: '',
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showEmergency, setShowEmergency] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.main_symptom.trim()) return;
    setLoading(true);
    try {
      const response = await symptomsAPI.check(formData);
      setResult(response);
      if (response.is_emergency) {
        setShowEmergency(true);
      }
    } catch (err) {
      console.error('Symptom check error:', err);
      if (err.response) {
        console.error('Backend error response:', err.response.data);
        setResult({
          reply: `Error: ${JSON.stringify(err.response.data)}. Please try again.`,
          risk_level: 'low',
          follow_up_questions: [],
          is_emergency: false
        });
      } else {
        setResult({
          reply: 'Error checking symptoms. Please try again.',
          risk_level: 'low',
          follow_up_questions: [],
          is_emergency: false
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Symptom Checker</h1>
        <p className="text-gray-600 mb-6">
          Provide details about your symptoms for general health information and guidance.
        </p>

        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Main Symptom *</label>
            <input
              type="text"
              name="main_symptom"
              value={formData.main_symptom}
              onChange={handleChange}
              required
              className="input-field"
              placeholder="e.g., headache, chest pain, cough"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Duration</label>
              <select name="duration" value={formData.duration} onChange={handleChange} className="input-field">
                <option value="">Select duration</option>
                <option value="just started">Just started</option>
                <option value="hours">A few hours</option>
                <option value="1-2 days">1-2 days</option>
                <option value="3-7 days">3-7 days</option>
                <option value="1-2 weeks">1-2 weeks</option>
                <option value="2-4 weeks">2-4 weeks</option>
                <option value="more than a month">More than a month</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Severity</label>
              <select name="severity" value={formData.severity} onChange={handleChange} className="input-field">
                <option value="">Select severity</option>
                <option value="mild">Mild</option>
                <option value="moderate">Moderate</option>
                <option value="severe">Severe</option>
                <option value="very severe">Very Severe</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Age Group</label>
              <select name="age_group" value={formData.age_group} onChange={handleChange} className="input-field">
                <option value="">Select age group</option>
                <option value="child (0-12)">Child (0-12)</option>
                <option value="teenager (13-17)">Teenager (13-17)</option>
                <option value="adult (18-64)">Adult (18-64)</option>
                <option value="senior (65+)">Senior (65+)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Other Symptoms</label>
            <textarea
              name="other_symptoms"
              value={formData.other_symptoms}
              onChange={handleChange}
              className="input-field"
              rows={2}
              placeholder="Any additional symptoms you're experiencing"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Existing Conditions</label>
              <textarea
                name="existing_conditions"
                value={formData.existing_conditions}
                onChange={handleChange}
                className="input-field"
                rows={2}
                placeholder="Any pre-existing medical conditions"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Current Medications</label>
              <textarea
                name="medications"
                value={formData.medications}
                onChange={handleChange}
                className="input-field"
                rows={2}
                placeholder="Any medications you're currently taking"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Recent Triggers or Changes</label>
            <input
              type="text"
              name="triggers"
              value={formData.triggers}
              onChange={handleChange}
              className="input-field"
              placeholder="e.g., new medication, stress, travel, diet change"
            />
          </div>

          <button type="submit" disabled={loading || !formData.main_symptom.trim()} className="btn-primary w-full py-3">
            {loading ? 'Analyzing...' : 'Check Symptoms'}
          </button>
        </form>

        {result && (
          <div className="mt-6 card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Results</h2>
            <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium mb-4 ${
              result.risk_level === 'low' ? 'bg-green-100 text-green-800' :
              result.risk_level === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
              result.risk_level === 'high' ? 'bg-orange-100 text-orange-800' :
              'bg-red-100 text-red-800'
            }`}>
              Risk Level: {result.risk_level.toUpperCase()}
            </div>
            <div className="prose prose-sm max-w-none text-gray-700">
              <ReactMarkdown>{result.reply}</ReactMarkdown>
            </div>
            {result.follow_up_questions?.length > 0 && (
              <div className="mt-4">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Follow-up Questions:</h3>
                <div className="flex flex-wrap gap-2">
                  {result.follow_up_questions.map((q: string, i: number) => (
                    <span key={i} className="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full">
                      {q}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800">
              This is general health information, not a medical diagnosis. Always consult a healthcare professional.
            </div>
          </div>
        )}

        <EmergencyWarning
          isVisible={showEmergency}
          message={result?.reply}
          onClose={() => setShowEmergency(false)}
        />
      </div>
    </Layout>
  );
};

export default SymptomCheckerPage;
