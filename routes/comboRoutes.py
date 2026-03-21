from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from services.comboService import llm_combo_suggest
from utils.get_current_user import get_current_user

class MenuOut(BaseModel):
    id_item: int
    name: str
    description: Optional[str]
    price: float
    cost: Optional[float]
    profit_margin: Optional[float]
    id_category: Optional[int]
    is_available: bool
    created_at: datetime

    class Config:
        orm_mode = True

class ComboResponse(BaseModel):
    items: List[MenuOut] = []
    message: Optional[str] = None

router = APIRouter(prefix="/combo", tags=["combo"])

@router.get("/{item_name}", response_model=ComboResponse)
def combo_(item_name: str, current_user = Depends(get_current_user)):
    return llm_combo_suggest(item_name)