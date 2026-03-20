from utils.user_preferences import get_user_preferences
from utils.user_history import get_user_history
from utils.find_user import find_user

def rank_with_preferences(items, user_email):
    pref_scores = {}
    history_scores = {}

    user = find_user(user_email)

    prefs = get_user_preferences(user.id_user)
    for p in prefs:
        value = p["preference_value"]
        confidence = p["confidence_score"] or 0
        pref_scores[value] = max(pref_scores.get(value, 0), confidence)

    history = get_user_history(user.id_user)
    if history:
        for i, intent in enumerate(history):
            weight = 1 - (i / len(history))
            history_scores[intent] = max(history_scores.get(intent, 0), weight)

    max_profit = max((float(i.profit_margin or 0) for i in items), default=1)

    ranked_items = []

    for item in items:
        profit_raw = float(item.profit_margin or 0)
        profit_score = (profit_raw / max_profit) if max_profit > 0 else 0

        preference_score = pref_scores.get(item.name, 0)
        if hasattr(item, "category"):
            preference_score = max(preference_score, pref_scores.get(item.category, 0))
        if hasattr(item, "tags"):
            for tag in item.tags:
                preference_score = max(preference_score, pref_scores.get(tag, 0))

        history_score = history_scores.get(item.name, 0)
        if hasattr(item, "category"):
            history_score = max(history_score, history_scores.get(item.category, 0))
        if hasattr(item, "tags"):
            for tag in item.tags:
                history_score = max(history_score, history_scores.get(tag, 0))

        score = (
            0.4 * profit_score +
            0.4 * preference_score +
            0.2 * history_score
        )

        if item.name in history_scores:
            score *= 0.9

        score = min(score, 1.0)

        ranked_items.append((item, score))

    ranked_items.sort(key=lambda x: x[1], reverse=True)

    return [item for item, score in ranked_items]