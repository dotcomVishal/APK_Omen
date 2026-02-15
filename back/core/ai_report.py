import os
import json
from groq import Groq

# client = Groq(api_key=os.environ.get(""))

MODEL_NAME = "llama-3.3-70b-versatile"


def build_prompt(apk_json):
    return f"""
You are an advanced mobile application security analysis engine.

You are provided with structured APK analysis data in JSON format.

CRITICAL RULES:

• Analyze EVERYTHING present in the JSON
• DO NOT omit any data
• DO NOT filter findings
• DO NOT ignore URLs, APIs, permissions, components, crypto, secrets, configs
• Even LOW confidence risks MUST be mentioned

You must distinguish between:

- Observed Risks
- Potential Attack Scenarios
- Technical Evidence & Triggers

---

OUTPUT FORMAT (STRICT):

Security Analysis Report
========================

1. Security Posture Overview

2. Observed Risks

3. Potential Attack Scenarios

4. Technical Evidence & Triggers

5. Sensitive Artifacts Identified

    5.1 URLs / Endpoints
    5.2 Sensitive Permissions
    5.3 Exported Components
    5.4 Cryptographic Indicators
    5.5 Secrets / Hardcoded Data

6. OWASP Mobile Top 10 Mapping

7. Risk Severity Assessment

8. Prioritized Recommendations

---

Here is the APK analysis JSON:

{json.dumps(apk_json, indent=2)}
"""


def generate_ai_report(apk_json):

    if not client:
        return "AI analysis unavailable. GROQ_API_KEY not configured."

    try:
        prompt = build_prompt(apk_json)

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {str(e)}"

