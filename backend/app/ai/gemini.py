import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-3-flash-preview")


def extract_json(text: str):
    """
    Safely extract JSON from Gemini response
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in response")
    return json.loads(match.group())


def analyze_symptoms(symptom_text: str, severity: str, area: str, city: str, country: str):
    location = f"{area}, {city}, {country}"
    prompt = f"""
You are a health assistant AI. A user has provided the following information about their symptoms:

Symptoms:
{symptom_text}

Severity:
{severity}

User location:
{location}

Tasks:
1. Explain the symptoms briefly.
2. Give a short summary.
3. List possible conditions (non-diagnostic).
4. Suggest lifestyle tips.
5. Suggest reminders.
6. Suggest recommended actions.
7. Suggest ONE AI-generated nearby doctor.

STRICT RULES:
- The doctor's city MUST be exactly: {city}
- The doctor's country MUST be exactly: {country}
- The doctor's area MUST be relevant to: {area}
- Do NOT mention USA or any other country.
- Do NOT invent random cities.
- Location must be realistic and relevant to the user's location.


IMPORTANT RULES:
- The doctor suggestion is AI-generated and may not be real.
- Clearly mark it as an AI-suggested doctor.
- Do NOT claim medical certainty.

Respond ONLY in valid JSON with this structure:
{{
  "explain_symptoms": "brief explanation of symptoms in wellness context",
  "summary": "short wellness summary",
  "possible_conditions": ["general non-diagnostic terms"],
  "lifestyle_tips": ["relevant lifestyle tips (diet, exercise, sleep, etc.)"],
  "remind_medication_appointments": ["general reminders to take medications and attend appointments"],
  "recommended_actions": ["specific lifestyle or care actions"],
  "nearest_doctor": {{
    "name": "",
    "specialty": "",
    "location": ""
  }},
  "disclaimer": "This is not medical advice."
}}
"""

    response = model.generate_content(prompt)

    # Debug (optional, useful for viva)
    print("RAW GEMINI RESPONSE:")
    print(response.text)

    try:
        return extract_json(response.text)

    except Exception as e:
        print("JSON PARSE ERROR:", e)

        return {
            "explain_symptoms": "brief explanation of symptoms in wellness context",
            "summary": "General wellness guidance based on symptoms.",
            "possible_conditions": ["General wellness concern"],
            "lifestyle_tips": ["relevant lifestyle tips (diet, exercise, sleep, etc.)"],
            "remind_medication_appointments": ["general reminders to take medications and attend appointments"],
            "recommended_actions": [
                "Monitor symptoms",
                "Maintain hydration",
                "Get adequate rest",
                "Consult a professional if symptoms worsen"
            ],
            "disclaimer": "This is not medical advice."
        }
