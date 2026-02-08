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

    try:
        result = analyze_symptoms(
            symptom_text=symptom.description,
            severity=symptom.severity
        )

        if not isinstance(result, dict):
            raise ValueError("Invalid AI response")

        return result

    except Exception as e:
        print("AI ERROR:", e)

        return {
            "summary": "AI service is temporarily unavailable.",
            "possible_conditions": ["General wellness concern"],
            "recommended_actions": [
                "Monitor symptoms",
                "Maintain hydration",
                "Consult a professional if symptoms persist"
            ],
            "disclaimer": "This is not medical advice."
        }

