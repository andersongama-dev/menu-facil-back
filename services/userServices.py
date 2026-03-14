from fastapi import HTTPException
from database.connection import SessionLocal
from models.user import UserORM

def add_user(name: str, email: str, phone: str):
    session = SessionLocal()
    try:
        exists = session.query(UserORM).filter(UserORM.email == email).first()
        if exists:
            raise HTTPException(status_code=409, detail="Email já cadastrado")
        new_user = UserORM(
            name=name,
            email=email,
            phone=phone
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    finally:
        session.close()

def find_user(email: str):
    session = SessionLocal()
    try:
        user_orm = session.query(UserORM).filter(UserORM.email == email).first()
        if not user_orm:
            raise HTTPException(status_code=404, detail="Usuário não encotrado")
        return user_orm
    finally:
        session.close()