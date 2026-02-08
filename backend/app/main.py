from fastapi import FastAPI
from .database import Base, engine
from .routes import users, symptoms, ai_analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediAssist AI Backend")

app.include_router(users.router)
app.include_router(symptoms.router)
app.include_router(ai_analysis.router)
