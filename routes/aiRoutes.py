from fastapi import APIRouter, Query
from services.aiService import ai_suggest_menu as ai_suggest

router = APIRouter()

@router.get("/ai/suggest")
def suggest(user_text: str = Query(..., description="Texto do usuário sobre prato desejado")):
    return ai_suggest(user_text)