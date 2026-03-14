from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter
import services.orderService as serviceOrder

class OrderCreate(BaseModel):
    id_user: UUID
    total_price: float

class OrderOut(BaseModel):
    id_order: int
    id_user: UUID
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True



router = APIRouter(prefix="/order", tags=["order"])

@router.post("/", response_model=OrderOut)
def new_order(order: OrderCreate):
    return serviceOrder.create_order(order.id_user, order.total_price)

@router.get("/{user_id}", response_model=list[OrderOut])
def all_orders(user_id):
    return serviceOrder.find_order(user_id)