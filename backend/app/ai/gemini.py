import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-3-flash-preview")


def extract_json(text: str):
    """
    Safely extract JSON from Gemini response
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in response")
    return json.loads(match.group())


def analyze_symptoms(symptom_text: str, severity: str):
    prompt = f"""
You are an AI wellness assistant.
You must NOT diagnose diseases.
You must NOT suggest medicines.
Give non-diagnostic, wellness-focused guidance.

Symptoms:
{symptom_text}

Severity:
{severity}

Respond ONLY in valid JSON with this structure:
{{
  "summary": "short wellness summary",
  "possible_conditions": ["general non-diagnostic terms"],
  "recommended_actions": ["specific lifestyle or care actions"],
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
            "summary": "General wellness guidance based on symptoms.",
            "possible_conditions": ["General wellness concern"],
            "recommended_actions": [
                "Monitor symptoms",
                "Maintain hydration",
                "Get adequate rest",
                "Consult a professional if symptoms worsen"
            ],
            "disclaimer": "This is not medical advice."
        }
