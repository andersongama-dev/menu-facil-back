from utils.ai import get_user_preferences


def rank_with_preferences(items, user_id=None):
    pref_scores = {}
    if user_id:
        prefs = get_user_preferences(user_id)
        for p in prefs:
            pref_scores[p["preference_value"]] = p["confidence_score"]
    ranked_items = []
    for item in items:
        profit = float(item.profit_margin or 0)
        preference = float(pref_scores.get(item.name, 0))
        score = 0.7 * profit + 0.3 * preference
        ranked_items.append((item, score))

    ranked_items.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in ranked_items]