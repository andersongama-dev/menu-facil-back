from utils.ranking import rank_with_preferences
from utils.items import fetch_all_menu_items

def user_suggest(user_id):
    items = fetch_all_menu_items()

    ranked_item = rank_with_preferences(items, user_id)

    return ranked_item[:4]


