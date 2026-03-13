from database.connection import get_connection

def new_order(user_id, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (id_user, total_price) VALUES (?, ?)", (user_id, price,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Pedido finalizado"}