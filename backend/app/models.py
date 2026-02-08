from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    symptoms = relationship("Symptom", back_populates="user")


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="symptoms")
