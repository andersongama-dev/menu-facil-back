from fastapi import APIRouter
from pydantic import BaseModel
import services.userServices as serviceUser

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login",)
def login(user: UserLogin):
    token = serviceUser.find_user(user.email, user.password)
    return {"access_token": token}

@router.post("/register")
def register(user: UserCreate):
    token = serviceUser.add_user(user.name, user.email, user.password)
    return {"access_token": token}