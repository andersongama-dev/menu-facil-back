from starlette.middleware.cors import CORSMiddleware

import models
from fastapi import FastAPI
from routes.userRoutes import router as user_routes
from routes.menuRoutes import router as menu_routes
from routes.orderRoutes import router as order_routes
from routes.aiRoutes import router as ai_suggest
from routes.suggestRoutes import router as user_suggest
from routes.comboRoutes import router as combo_suggest
from routes.scoretimeRoutes import router as score_time
import uvicorn

app = FastAPI()

pp = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(menu_routes)
app.include_router(order_routes)
app.include_router(ai_suggest)
app.include_router(user_suggest)
app.include_router(combo_suggest)
app.include_router(score_time)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)