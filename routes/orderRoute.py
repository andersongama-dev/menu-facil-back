from fastapi import APIRouter
import services.orderService as serviceOrder
from models.order import Order

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/")
def new(order: Order):
    return serviceOrder.new_order(order.id_user, order.total_price)