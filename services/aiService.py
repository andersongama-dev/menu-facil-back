from utils.intent_parser import parse_user_intent
from utils.menu_filter import filter_menu
from utils.ranking import rank_with_preferences
from utils.upsell import get_upsells
from utils.ai import llm_select
from utils.items import fetch_all_menu_items
from models.ai import AIORM
from models.user_preference import UserPreferenceORM
from database.connection import SessionLocal

def ai_suggest_menu(user_input: str, user_id, context=""):

    items = fetch_all_menu_items()

    intent = parse_user_intent(user_input)

    filtered = filter_menu(items, intent)

    parsed_intent = intent

    ranked = rank_with_preferences(filtered, user_id)
    candidates = ranked[:10]

    selected = llm_select(candidates, user_input, context, user_id=user_id)

    drink, dessert = get_upsells(items)

    try:
        save_ia(user_id, user_input, parsed_intent)
        if selected and selected[0].category:
            category_name = selected[0].category.name or f"Categoria_{selected[0].category.id_category}"
            save_preference(
                user_id=user_id,
                preference_type=category_name,
                preference_value=selected[0].name
            )
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

def save_preference(user_id, preference_type, preference_value):
    session = SessionLocal()
    try:
        prefs = session.query(UserPreferenceORM).filter(
            UserPreferenceORM.id_user == user_id,
            UserPreferenceORM.preference_type == preference_type
        ).all()
        matched = next((p for p in prefs if p.preference_value == preference_value), None)
        if matched:
            matched.confidence_score = 1.00
        else:
            matched = UserPreferenceORM(
                id_user=user_id,
                preference_type=preference_type,
                preference_value=preference_value,
                confidence_score=1.00
            )
            session.add(matched)
            prefs.append(matched)
        other_prefs = [p for p in prefs if p != matched]
        for p in other_prefs:
            score = float(p.confidence_score)
            p.confidence_score = max(score * 0.5, 0.10)
        session.commit()
    finally:
        session.close()