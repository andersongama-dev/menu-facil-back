from fastapi import HTTPException

from models.user import UserORM
from database.connection import SessionLocal

def find_user(user_email) -> UserORM:
    session = SessionLocal()
    exists = session.query(UserORM).filter(UserORM.email == user_email).first()
    session.close()
    if not exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return exists