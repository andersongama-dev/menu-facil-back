from fastapi import APIRouter, Query, Depends
from services.aiService import ai_suggest_menu
from utils.get_current_user import get_current_user

router = APIRouter()

@router.get("/ai/suggest", tags=["suggest IA"])
def suggest(user_text: str = Query(..., description="Texto do usuário sobre prato desejado"),
            current_user: str = Depends(get_current_user)):
    return ai_suggest_menu(user_text, current_user)