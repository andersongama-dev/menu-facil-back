from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
import services.suggestService as serviceSuggest
from pydantic import RootModel
from uuid import UUID

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

@router.get("/{user_id}", response_model=MenuListResponse)
def suggest(user_id: UUID):
    items = serviceSuggest.user_suggest(user_id)
    return MenuListResponse(root=items)