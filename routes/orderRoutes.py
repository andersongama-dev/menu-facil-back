from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, Depends
import services.orderService as serviceOrder
from utils.get_current_user import get_current_user

class OrderCreate(BaseModel):
    total_price: float

class OrderOut(BaseModel):
    id_order: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True



router = APIRouter(prefix="/order", tags=["order"])

@router.post("/", response_model=OrderOut)
def new_order(order: OrderCreate, current_user: str = Depends(get_current_user)):
    return serviceOrder.create_order(current_user, order.total_price)

@router.get("/me", response_model=list[OrderOut])
def all_orders(current_user: str = Depends(get_current_user)):
    return serviceOrder.find_order(current_user)