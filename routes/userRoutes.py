from fastapi import APIRouter
import services.userServices as serviceUser
from models.user import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/login/{user_email}", response_model=User)
def login(user_email: str) -> User:
    return serviceUser.find_user(user_email)

@router.post("/register")
def register(user: User):
    user_id = serviceUser.add_user(user.name, user.email, user.phone)
    return {"message": "Usuário registrado com sucesso", "id_user": user_id}