def rank_by_profit(items):

    return sorted(
        items,
        key=lambda x: x.profit_margin,
        reverse=True
    )