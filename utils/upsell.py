def get_upsells(items):
    drinks = [i for i in items if getattr(i, "id_category", None) == 3]
    desserts = [i for i in items if getattr(i, "id_category", None) == 4]

    drink = max(drinks, key=lambda x: float(x.profit_margin or 0), default=None)
    dessert = max(desserts, key=lambda x: float(x.profit_margin or 0), default=None)

    return drink, dessert