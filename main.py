from fastapi import FastAPI

app = FastAPI()


pratos = []

@app.get("/")
def root():
    return {"Hello": "Word"}

@app.post("/pratos")
def createPrato(prato: str):
    pratos.append(prato)
    return pratos