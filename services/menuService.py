from fastapi import HTTPException
from database.connection import get_connection
from models.menu import Menu

def list_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT id_item, name, description, price, cost, profit_margin, id_category FROM menu_items""")
    rows = cursor.fetchall()
    menu_items = []
    for row in rows:
        item = Menu(
            id_item=row[0],
            name=row[1],
            description=row[2],
            price=row[3],
            cost=row[4],
            profit_margin=row[5],
            id_category=row[6]
        )
        menu_items.append(item)
    cursor.close()
    conn.close()
    return menu_items

def find_menu_item(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_item, name, description, price, cost, profit_margin, id_category FROM menu_items WHERE id_item = ?
    """, (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return Menu(
            id_item=row[0],
            name=row[1],
            description=row[2],
            price=row[3],
            cost=row[4],
            profit_margin=row[5],
            id_category=row[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Menu não encotrado")
