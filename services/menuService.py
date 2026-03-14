from fastapi import HTTPException
from database.connection import SessionLocal
from models import MenuORM, CategoryORM

def list_menu():
    session = SessionLocal()
    try:
        items = session.query(MenuORM).all()
        if not items:
            raise HTTPException(status_code=404, detail="Nenhum menu encontrado")
        return items
    finally:
        session.close()

def find_menu_item(menu_id: int):
    session = SessionLocal()
    try:
        item = session.query(MenuORM).filter(MenuORM.id_item == menu_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Menu não encontrado")
        return item
    finally:
        session.close()