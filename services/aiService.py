from utils.intent_parser import parse_user_intent
from utils.menu_filter import filter_menu
from utils.ranking import rank_by_profit
from utils.upsell import get_upsells
from utils.ai import llm_select
from utils.items import fetch_all_menu_items


def ai_suggest_menu(user_input: str, context=""):

    items = fetch_all_menu_items()

    intent = parse_user_intent(user_input)

    filtered = filter_menu(items, intent)

    ranked = rank_by_profit(filtered)

    candidates = ranked[:10]

    selected = llm_select(candidates, user_input, context)

    drink, dessert = get_upsells(items)

    return {
        "recommendations": selected,
        "upsell": {
            "drink": drink,
            "dessert": dessert
        }
    }