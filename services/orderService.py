from database.connection import SessionLocal
from models.order import OrderORM
from utils.find_user import find_user


def create_order(user_email, price):
    session = SessionLocal()
    try:
        user = find_user(user_email)
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
        user = find_user(user_email)
        orders = session.query(OrderORM).filter(OrderORM.id_user == user.id_user).all()
        return orders
    finally:
        session.close()