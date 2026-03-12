from pydantic import BaseModel

class Menu(BaseModel):
    id_item: int | None = None
    name: str
    description: str
    price: float
    cost: float
    profit_margin: float
    id_category: int
