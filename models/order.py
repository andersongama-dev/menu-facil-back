from pydantic import BaseModel

class Order(BaseModel):
    id_order: int | None = None
    id_user: int
    total_price: float