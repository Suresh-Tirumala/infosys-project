import json
import logging
from typing import Dict, Any, List
from groq import Groq
from django.conf import settings
from core.prompts.general import GENERAL_HEALTH_SYSTEM
from core.prompts.symptom_analysis import SYMPTOM_ANALYSIS_SYSTEM
from core.prompts.emergency import EMERGENCY_DETECTION_SYSTEM
from core.prompts.document_explanation import DOCUMENT_EXPLANATION_SYSTEM
from core.prompts.health_summary import HEALTH_SUMMARY_SYSTEM
from core.prompts.medication import MEDICATION_INFO_SYSTEM

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)

    def _call_llm(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        if not self.client:
            return json.dumps({
                "response": "AI service is temporarily unavailable. Please try again later.",
                "risk_level": "low",
                "follow_up_questions": [],
                "safety_warnings": [],
                "is_emergency": False
            })

        try:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=full_messages,
                temperature=temperature,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return json.dumps({
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again shortly.",
                "risk_level": "low",
                "follow_up_questions": [],
                "safety_warnings": ["Unable to process at this time"],
                "is_emergency": False
            })

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except (json.JSONDecodeError, IndexError):
            return {
                "response": response,
                "risk_level": "low",
                "follow_up_questions": [],
                "safety_warnings": [],
                "possible_explanations": [],
                "self_care_suggestions": [],
                "warning_signs": [],
                "when_to_see_doctor": "Consult a healthcare professional if symptoms persist."
            }

    def check_emergency(self, message: str) -> Dict[str, Any]:
        messages = [{"role": "user", "content": f"Assess this message for emergency: {message}"}]
        response = self._call_llm(EMERGENCY_DETECTION_SYSTEM, messages, temperature=0.3)
        parsed = self._parse_json_response(response)
        return {
            "is_emergency": parsed.get("is_emergency", False),
            "emergency_type": parsed.get("emergency_type", ""),
            "immediate_action": parsed.get("immediate_action", ""),
            "risk_level": parsed.get("risk_level", "low"),
            "message": parsed.get("message", "")
        }

    def general_health_chat(self, messages: List[Dict], health_context: str = "") -> Dict[str, Any]:
        context_msg = []
        if health_context:
            context_msg.append({"role": "system", "content": f"User health profile context: {health_context}"})
        context_msg.extend(messages)
        response = self._call_llm(GENERAL_HEALTH_SYSTEM, context_msg)
        parsed = self._parse_json_response(response)
        return parsed

    def analyze_symptoms(self, symptom_data: Dict[str, Any], conversation_history: List[Dict] = None) -> Dict[str, Any]:
        symptom_text = f"""
Symptom Analysis Request:
- Main Symptom: {symptom_data.get('main_symptom', 'Not specified')}
- Duration: {symptom_data.get('duration', 'Not specified')}
- Severity: {symptom_data.get('severity', 'Not specified')}
- Age Group: {symptom_data.get('age_group', 'Not specified')}
- Existing Conditions: {symptom_data.get('existing_conditions', 'None specified')}
- Current Medications: {symptom_data.get('medications', 'None specified')}
- Other Symptoms: {symptom_data.get('other_symptoms', 'None specified')}
- Recent Triggers/Changes: {symptom_data.get('triggers', 'None specified')}
"""
        messages = [{"role": "user", "content": symptom_text}]
        if conversation_history:
            messages = conversation_history + messages
        response = self._call_llm(SYMPTOM_ANALYSIS_SYSTEM, messages)
        return self._parse_json_response(response)

    def explain_document(self, document_text: str, user_question: str = "") -> Dict[str, Any]:
        content = f"Medical Document Content:\n{document_text}"
        if user_question:
            content += f"\n\nUser Question: {user_question}"
        messages = [{"role": "user", "content": content}]
        response = self._call_llm(DOCUMENT_EXPLANATION_SYSTEM, messages)
        return self._parse_json_response(response)

    def generate_summary(self, conversation_messages: List[Dict]) -> Dict[str, Any]:
        conversation_text = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in conversation_messages
        ])
        messages = [{"role": "user", "content": f"Generate a health report summary for this conversation:\n\n{conversation_text}"}]
        response = self._call_llm(HEALTH_SUMMARY_SYSTEM, messages)
        return self._parse_json_response(response)

    def medication_info(self, question: str, health_context: str = "") -> Dict[str, Any]:
        content = f"Medication Question: {question}"
        if health_context:
            content += f"\n\nUser Health Context: {health_context}"
        messages = [{"role": "user", "content": content}]
        response = self._call_llm(MEDICATION_INFO_SYSTEM, messages)
        return self._parse_json_response(response)


ai_service = AIService()
