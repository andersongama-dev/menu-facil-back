from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from services.scoretimeService import recommend_menu_by_location
from utils.get_current_user import get_current_user

router = APIRouter(prefix="/weather-menu", tags=["Weather Menu"])

class WeatherMenuRequest(BaseModel):
    lat: float
    lon: float

class MenuItemOut(BaseModel):
    id_item: int
    name: str
    description: str | None
    price: float | None
    cost: float | None
    profit_margin: float | None
    id_category: int | None
    is_available: bool | None
    created_at: datetime | None

    class Config:
        orm_mode = True

class WeatherMenuResponse(BaseModel):
    temperature: float
    dishes: List[MenuItemOut]

@router.post("", response_model=WeatherMenuResponse)
def get_weather_menu(request: WeatherMenuRequest, current_user: str = Depends(get_current_user)):
    try:
        result = recommend_menu_by_location(request.lat, request.lon, current_user)
        return {
            "temperature": result["temperature"],
            "dishes": result["dishes"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))