from utils.upsell import get_upsells
from utils.ai import llm_select
from utils.items import fetch_all_menu_items
from models.ai import AIORM
from models.user_preference import UserPreferenceORM
from database.connection import SessionLocal
from utils.find_user import find_user

def ai_suggest_menu(user_input: str, user_email,):
    items = fetch_all_menu_items()

    selected = llm_select(items, user_input)

    drink, dessert = get_upsells(items)

    try:
        user = find_user(user_email)

        save_interaction(user_email, user_input)

        if selected and selected[0].category:
            category_name = selected[0].category.name or f"Categoria_{selected[0].category.id_category}"
            save_preference(user.id_user, category_name, selected[0].name)

    except Exception as e:
        print(f"Erro ao salvar interação: {e}")

    return {
        "recommendations": selected,
        "upsell": {
            "drink": drink,
            "dessert": dessert
        }
    }


def save_interaction(user_id, user_input):
    session = SessionLocal()
    try:
        new_ia = AIORM(
            id_user=user_id,
            input_text=user_input,
            parsed_intent=None
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
            matched.confidence_score = min(float(matched.confidence_score) + 0.2, 1.0)
        else:
            matched = UserPreferenceORM(
                id_user=user_id,
                preference_type=preference_type,
                preference_value=preference_value,
                confidence_score=0.2
            )
            session.add(matched)
            prefs.append(matched)

        for p in prefs:
            if p != matched:
                p.confidence_score = max(float(p.confidence_score) * 0.9, 0.05)

        session.commit()
    finally:
        session.close()