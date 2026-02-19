from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..crud import get_symptom
from ..ai.gemini import analyze_symptoms
from ..utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/analysis/{symptom_id}")
def analyze(symptom_id: int, db: Session = Depends(get_db)):
    logger.info(f"AI analysis requested for symptom_id: {symptom_id}")
    symptom = get_symptom(db, symptom_id)

    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")

    # 🔍 DEBUG PRINTS (VERY IMPORTANT)
    print("====================================")
    print("ANALYZING SYMPTOM ID:", symptom_id)
    print("SYMPTOM TEXT:", symptom.description)
    print("SEVERITY:", symptom.severity)
    print("====================================")
    # 📍 Extract user location safely
    area = city = country = "Unknown"

    if symptom.user and symptom.user.location and symptom.user.location != "None":
    # Split by comma and clean whitespace
        parts = [p.strip() for p in symptom.user.location.split(",") if p.strip()]
    
    # Dynamically assign based on what's available
        if len(parts) >= 3:
            area = parts[0]
            city = parts[1]
            country = parts[2]
        elif len(parts) == 2:
            city = parts[0]
            country = parts[1]
        elif len(parts) == 1:
            city = parts[0]
    try:
        result = analyze_symptoms(
            symptom_text=symptom.description,
            severity=symptom.severity,
            area=area,
            city=city,
            country=country
        )

        if not isinstance(result, dict):
            raise ValueError("Invalid AI response")

        return result

    except Exception as e:
        import traceback
        print("AI ERROR FULL TRACE:")
        traceback.print_exc()

        return {
            "explain_symptoms": "brief explanation of symptoms in wellness context",
            "summary": "AI service is temporarily unavailable.",
            "possible_conditions": ["General wellness concern"],
            "lifestyle_tips": ["Maintain a healthy lifestyle (diet, exercise, sleep)"],
            "remind_medication_appointments": ["Remember to take medications and attend appointments"],
            "recommended_actions": [
                "Monitor symptoms",
                "Maintain hydration",
                "Consult a professional if symptoms persist"
            ],
            "nearest_clinics": ["Find nearby clinics using a map service"],
            "disclaimer": "This is not medical advice."
        }

