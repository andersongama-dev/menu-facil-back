from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
import services.suggestService as serviceSuggest
from pydantic import RootModel
from utils.get_current_user import get_current_user

class MenuOut(BaseModel):
    id_item: int
    name: str
    description: Optional[str]
    price: float
    cost: Optional[float]
    profit_margin: Optional[float]
    is_available: bool
    id_category: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class MenuListResponse(RootModel):
    root: list[MenuOut]

router = APIRouter(prefix="/suggest", tags=["suggest"])

@router.get("", response_model=MenuListResponse)
def suggest(current_user = Depends(get_current_user)):
    items = serviceSuggest.user_suggest(current_user)
    return MenuListResponse(root=items)