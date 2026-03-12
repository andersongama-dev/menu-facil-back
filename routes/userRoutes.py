from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login():
    return {"message": "Fazer login"}

@router.post("/register")
def register():
    return {"message": "Fazer registro"}