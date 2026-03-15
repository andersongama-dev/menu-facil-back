from utils.intent_parser import parse_user_intent
from utils.menu_filter import filter_menu
from utils.ranking import rank_by_profit
from utils.upsell import get_upsells
from utils.ai import llm_select
from utils.items import fetch_all_menu_items
from models.ai import AIORM
from database.connection import SessionLocal

def ai_suggest_menu(user_input: str, user_id, context=""):

    items = fetch_all_menu_items()

    intent = parse_user_intent(user_input)

    filtered = filter_menu(items, intent)

    parsed_intent = intent

    ranked = rank_by_profit(filtered)

    candidates = ranked[:10]

    selected = llm_select(candidates, user_input, context)


    drink, dessert = get_upsells(items)

    try:
        save_ia(user_id, user_input, parsed_intent)
    except Exception as e:
        print(f"Erro ao salvar interação: {e}")

    return {
        "recommendations": selected,
        "upsell": {
            "drink": drink,
            "dessert": dessert
        }
    }

def save_ia(user_id, user_input, parsed_intent):
    session = SessionLocal()
    try:
        new_ia = AIORM(
            id_user=user_id,
            input_text=user_input,
            parsed_intent=parsed_intent
        )
        session.add(new_ia)
        session.commit()
    finally:
        session.close()