import uuid
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

import services.userServices as serviceUser

class UserOut(BaseModel):
    id_user: uuid.UUID
    name: str
    email: str
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/login/{user_email}", response_model=UserOut)
def login(user_email: str):
    user = serviceUser.find_user(user_email)
    return user

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    new_user = serviceUser.add_user(user.name, user.email, user.phone)
    return new_user