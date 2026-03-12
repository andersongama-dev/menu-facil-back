from  fastapi import APIRouter
import services.menuService as serviceMenu
from models.menu import Menu

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=list[Menu])
def all_menu():
    return serviceMenu.list_menu()

@router.get("/{id_menu}", response_model=Menu)
def find_menu(id_menu: int) -> Menu:
    return serviceMenu.find_menu_item(id_menu)