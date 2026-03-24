from typing import List, Dict
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

def fetch_all_menu_items_name() -> List[Dict]:
    session = SessionLocal()
    try:
        menu_all = session.query(MenuORM).options(selectinload(MenuORM.category)).all()
        if not menu_all:
            raise HTTPException(status_code=404, detail="Nenhum menu encontrado")

        return [
            {
                "name": item.name,
                "category": item.category.name if item.category else None,
                "description": item.description if item.description else None
            }
            for item in menu_all
        ]
    finally:
        session.close()


def fetch_menu_item_by_name(name: str) -> MenuORM:
    session = SessionLocal()
    try:
        all_items = session.query(MenuORM).options(selectinload(MenuORM.category)).all()
        if not all_items:
            raise HTTPException(status_code=404, detail="Nenhum item de menu encontrado")

        for item in all_items:
            if item.name == name:
                return item

        raise HTTPException(status_code=404, detail=f"Item '{name}' não encontrado")
    finally:
        session.close()