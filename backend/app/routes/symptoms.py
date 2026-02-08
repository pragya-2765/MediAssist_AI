from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, crud
from ..utils.logger import logger

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_symptom(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    logger.info(f"Symptom submitted for user_id: {symptom.user_id}")
    return crud.create_symptom(db, symptom)

@router.get("/user/{user_id}")
def get_user_symptoms(user_id: int, db: Session = Depends(get_db)):
    return crud.get_symptoms_by_user(db, user_id)

