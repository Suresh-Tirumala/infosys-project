import re
from typing import Dict, Any


class SafetyService:
    EMERGENCY_KEYWORDS = [
        r"\bchest\s*pain\b", r"\bheart\s*attack\b", r"\bstroke\b",
        r"\bsuicid", r"\bkill\s*(my)?self\b", r"\bself[\s-]*harm\b",
        r"\boverdose\b", r"\bpoison", r"\bchoking\b", r"\bcan'?t\s*breathe\b",
        r"\buncontrolle.*\bbleed", r"\bsevere.*\ballergic\b", r"\banaphyla",
        r"\bseizure", r"\bunconscious", r"\bloss\s*of\s*consciousness",
        r"\bblue\s*(lips|face|skin)\b", r"\bsevere.*\bpain\b.*\bchest\b",
        r"\brapid\s*heart", r"\bblood\s*pressure.*emergency",
        r"\bdifficulty\s*(breathing|speaking)\b", r"\bnumb.*\bface\b",
        r"\bslurred\s*speech\b", r"\bfacial\s*droop",
        r"\bsudden\s*(severe|worst)\s*headache\b",
    ]

    DANGEROUS_ADVICE_PATTERNS = [
        r"\bstop\s*(taking|your)\s*(medication|medicine|drug)",
        r"\bdiscontinue\s*(your|the)\s*(medication|medicine|drug)",
        r"\bdon'?t\s*take\s*(your|the)\s*(medication|medicine|drug)",
        r"\binject\s*(yourself|myself)\s*with",
        r"\btake\s*(more|extra|double)\s*(dose|doses)\b",
        r"\bself[\s-]*medicate\b",
    ]

    def check_emergency(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        for pattern in self.EMERGENCY_KEYWORDS:
            if re.search(pattern, text_lower):
                return {
                    "is_emergency": True,
                    "detected_pattern": pattern,
                    "message": "EMERGENCY DETECTED: Please seek immediate medical attention. Call emergency services (911/112/999) or go to the nearest emergency room immediately."
                }
        return {"is_emergency": False}

    def validate_ai_response(self, response: str, user_message: str = "") -> Dict[str, Any]:
        warnings = []
        modified_response = response

        for pattern in self.DANGEROUS_ADVICE_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                warnings.append(f"Potentially dangerous advice detected and flagged")
                modified_response = self._add_safety_disclaimer(modified_response)

        if not any(phrase in response.lower() for phrase in [
            "consult", "doctor", "healthcare professional", "medical professional",
            "not a diagnosis", "not medical advice", "seek professional"
        ]):
            warnings.append("Response may lack appropriate medical disclaimers")

        return {
            "is_safe": len(warnings) == 0,
            "warnings": warnings,
            "modified_response": modified_response
        }

    def _add_safety_disclaimer(self, response: str) -> str:
        disclaimer = "\n\nIMPORTANT SAFETY NOTICE: This is general information only. Always consult your healthcare professional before making any changes to your treatment plan. Never stop or change medication without medical supervision."
        return response + disclaimer

    def sanitize_input(self, text: str) -> str:
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"javascript:", "", text, flags=re.IGNORECASE)
        text = re.sub(r"on\w+\s*=", "", text, flags=re.IGNORECASE)
        return text.strip()

    def detect_prompt_injection(self, text: str) -> bool:
        injection_patterns = [
            r"ignore\s*(previous|all|above)\s*(instructions?|prompts?)",
            r"you\s*are\s*now\s*a",
            r"forget\s*(everything|all|previous)",
            r"new\s*instructions?:",
            r"system\s*prompt:",
            r"act\s*as\s*if",
            r"pretend\s*you\s*(are|'re)",
            r"bypass\s*(your|the)\s*(safety|rules|guidelines)",
        ]
        for pattern in injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


safety_service = SafetyService()
