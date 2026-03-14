from typing import List
from  models.menu import Menu
from database.connection import get_connection

def fetch_all_menu_items() -> List[Menu]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_item, name, description, price, cost, profit_margin, id_category
        FROM menu_items
        WHERE is_available = 1
    """)
    rows = cursor.fetchall()
    items = [
        Menu(
            id_item=row["id_item"],
            name=row["name"],
            description=row["description"],
            price=row["price"],
            cost=row["cost"],
            profit_margin=row["profit_margin"],
            id_category=row["id_category"]
        )
        for row in rows
    ]
    cursor.close()
    conn.close()
    return items