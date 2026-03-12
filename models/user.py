from pydantic import BaseModel

class User(BaseModel):
    id_user: int | None = None
    name: str
    email: str
    phone: str
