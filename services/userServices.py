from fastapi import HTTPException
from database.connection import SessionLocal
from models.user import UserORM
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-super-secreta")

def add_user(name: str, email: str, password):
    session = SessionLocal()
    try:
        exists = session.query(UserORM).filter(UserORM.email == email).first()
        if exists:
            raise HTTPException(status_code=409, detail="Email inválido")

        salt = bcrypt.gensalt(rounds=8)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        new_user = UserORM(
            name=name,
            email=email,
            password=password_hash
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return jwt_generate(email)
    finally:
        session.close()

def find_user(email: str, password):
    session = SessionLocal()
    try:
        user_orm = session.query(UserORM).filter(UserORM.email == email).first()
        if not user_orm:
            raise HTTPException(status_code=404, detail="Credenciais inválidas")
        if not bcrypt.checkpw(password.encode('utf-8'), user_orm.password):
            raise HTTPException(status_code=401, detail="Senha inválida")
        return jwt_generate(email)
    finally:
        session.close()


def jwt_generate(email):
    token = jwt.encode(
        {"user": email, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return token