import models
from fastapi import FastAPI
from routes.userRoutes import router as user_routes
from routes.menuRoutes import router as menu_routes
from routes.orderRoute import router as order_routes
from routes.aiRoutes import router as ai_suggest
import uvicorn

app = FastAPI()

app.include_router(user_routes)
app.include_router(menu_routes)
app.include_router(order_routes)
app.include_router(ai_suggest)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

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