from database.connection import SessionLocal
from models.order import OrderORM
from utils.find_user import find_user
from utils.genarete_qr_code import generate_qrcode_pix

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
        qr_path = generate_qrcode_pix("andersongamasilva08@gmail.com", "Anderson Gama Silva", "SerraNegra",
                                      price, tx_id="***", order_id=new_order.id_order)
        return {
            "order": new_order,
            "qr_path": qr_path
        }
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

def confirm_payment_order(user_email: str, order_id: int) -> OrderORM:
    session = SessionLocal()
    try:
        user = find_user(user_email)

        order = session.query(OrderORM).filter(
            OrderORM.id_order == order_id,
            OrderORM.id_user == user.id_user
        ).one_or_none()

        if not order:
            raise ValueError(f"Ordem {order_id} não encontrada para o usuário {user_email}")

        order.status = "paid"
        session.commit()
        session.refresh(order)
        return order

    finally:
        session.close()