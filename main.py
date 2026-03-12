from fastapi import FastAPI, HTTPException
from routes.userRoutes import router as user_routes

app = FastAPI()

app.include_router(user_routes)

#class Item(BaseModel):
#    text: str
#    is_done: bool = False

#pratos = []

#@app.get("/")
#def root():
#    return {"Hello": "Word"}

#@app.post("/pratos")
#def create_prato(prato: Item):
#    pratos.append(prato)
#    return pratos

#@app.get("/pratos", response_model=list[Item])
#def list_prato(limit: int = 10):
#    return pratos[0:limit]

#@app.get("/pratos/{prato_id}", response_model=Item)
#def get_prato(prato_id: int) -> Item:
#    if prato_id < len(pratos):
#        return pratos[prato_id]
#    else:
#        raise HTTPException(status_code=404, detail="Item not found")
#