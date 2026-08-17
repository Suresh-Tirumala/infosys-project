export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export interface HealthProfile {
  id: number;
  user_id: number;
  age: number | null;
  sex: string | null;
  height: number | null;
  weight: number | null;
  blood_type: string | null;
  allergies: string;
  existing_conditions: string;
  current_medications: string;
  emergency_contact: string;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: number;
  user_id: number;
  title: string;
  category: string;
  risk_level: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  role: string;
  content: string;
  risk_level: string;
  created_at: string;
}

export interface ChatResponse {
  reply: string;
  conversation_id: number;
  risk_level: string;
  follow_up_questions: string[];
  safety_warnings: string[];
  is_emergency: boolean;
}

export interface HealthCategory {
  id: string;
  name: string;
  icon: string;
  description: string;
}

export interface UploadedDocument {
  id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  summary: string;
  status: string;
  created_at: string;
}

export interface ReportSummary {
  id: number;
  user_id: number;
  conversation_id: number | null;
  symptoms_mentioned: string;
  duration: string;
  key_info: string;
  questions_discussed: string;
  guidance: string;
  warning_signs: string;
  next_steps: string;
  created_at: string;
}

export interface UserSettings {
  language: string;
  theme: string;
  voice_enabled: boolean;
  notification_enabled: boolean;
  data_retention_days: number;
  share_analytics: boolean;
}

export interface EmergencyWarning {
  is_emergency: boolean;
  message: string;
  immediate_action: string;
}
