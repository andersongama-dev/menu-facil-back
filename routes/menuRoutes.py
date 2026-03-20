from  fastapi import APIRouter, Depends
import services.menuService as serviceMenu
from pydantic import BaseModel
from datetime import datetime
from utils.get_current_user import get_current_user

class MenuOut(BaseModel):
    id_item: int
    name: str
    description: str | None
    price: float
    cost: float | None
    profit_margin: float | None
    id_category: int | None
    is_available: bool
    created_at: datetime

    class Config:
        orm_mode = True

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=list[MenuOut])
def get_menu(current_user: str = Depends(get_current_user)):
    return serviceMenu.list_menu()

@router.get("/{menu_id}", response_model=MenuOut)
def get_menu_item(menu_id: int, current_user: str = Depends(get_current_user)):
    return serviceMenu.find_menu_item(menu_id)