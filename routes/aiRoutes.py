from fastapi import APIRouter, Query
from services.aiService import ai_suggest_menu

router = APIRouter()

@router.get("/ai/suggest")
def suggest(
    user_text: str = Query(..., description="Texto do usuário sobre prato desejado"),
    user_id: str = Query(..., description="ID do usuário"),
    context: str = Query("", description="Histórico da conversa anterior")
):
    return ai_suggest_menu(user_text, user_id, context)