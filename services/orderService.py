from fastapi import HTTPException
from database.connection import SessionLocal
from models.order import OrderORM
from models.user import UserORM


def create_order(user_email, price):
    session = SessionLocal()
    try:
        user = find_user(session, user_email)
        new_order = OrderORM(
            id_user=user.id_user,
            total_price=price
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return new_order
    finally:
        session.close()


def find_order(user_email):
    session = SessionLocal()
    try:
        user = find_user(session, user_email)
        orders = session.query(OrderORM).filter(OrderORM.id_user == user.id_user).all()
        return orders
    finally:
        session.close()


def find_user(session, user_email) -> UserORM:
    exists = session.query(UserORM).filter(UserORM.email == user_email).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return exists