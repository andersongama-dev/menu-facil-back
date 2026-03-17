from utils.user_preferences import get_user_preferences

def rank_with_preferences(items, user_id=None):
    pref_scores = {}
    if user_id:
        prefs = get_user_preferences(user_id)
        for p in prefs:
            pref_scores[p["preference_value"]] = p["confidence_score"] or 0

    ranked_items = []
    for item in items:
        profit = float(item.profit_margin or 0)
        base_score = 0.7 * profit

        preference_score = float(pref_scores.get(item.name, 0))
        if preference_score > 0:
            score = base_score + 0.2
            score = min(score, 1)
        else:
            score = base_score * 0.9

        ranked_items.append((item, score))

    ranked_items.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in ranked_items]