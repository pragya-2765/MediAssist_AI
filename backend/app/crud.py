from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(full_name=user.full_name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_symptom(db: Session, symptom: schemas.SymptomCreate):
    db_symptom = models.Symptom(**symptom.dict())
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom

def get_symptoms_by_user(db: Session, user_id: int):
    return db.query(models.Symptom).filter(models.Symptom.user_id == user_id).all()

def get_symptom(db: Session, symptom_id: int):
    return db.query(models.Symptom).filter(models.Symptom.id == symptom_id).first()
