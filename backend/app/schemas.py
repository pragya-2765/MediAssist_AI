from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    email: str
    location: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    location: str

    class Config:
        orm_mode = True


class SymptomCreate(BaseModel):
    user_id: int
    description: str
    severity: str

class SymptomOut(BaseModel):
    id: int
    description: str
    severity: str
    user_id: int

    class Config:
        orm_mode = True
