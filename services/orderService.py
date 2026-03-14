from fastapi import HTTPException
from database.connection import SessionLocal
from models.order import OrderORM
from models.user import UserORM


def create_order(user_id, price):
    session = SessionLocal()
    try:
        find_user(session, user_id)
        new_order = OrderORM(
            id_user=user_id,
            total_price=price
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        return new_order
    finally:
        session.close()


def find_order(user_id):
    session = SessionLocal()
    try:
        find_user(session, user_id)
        orders = session.query(OrderORM).filter(OrderORM.id_user == user_id).all()
        return orders
    finally:
        session.close()


def find_user(session, user_id):
    exists = session.query(UserORM).filter(UserORM.id_user == user_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return exists