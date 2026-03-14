from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from  models.menu import MenuORM
from database.connection import SessionLocal

def fetch_all_menu_items() -> List[MenuORM]:
    session = SessionLocal()
    try:
        menu_all = session.query(MenuORM).options(selectinload(MenuORM.category)).all()
        if not menu_all:
            raise HTTPException(status_code=404, detail="Nenhum menu encontrado")
        return menu_all
    finally:
        session.close()