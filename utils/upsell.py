def get_upsells(items):

    drinks = [i for i in items if i.id_category == 3]
    desserts = [i for i in items if i.id_category == 4]

    drink = None
    dessert = None

    if drinks:
        drink = max(drinks, key=lambda x: x.profit_margin)

    if desserts:
        dessert = max(desserts, key=lambda x: x.profit_margin)

    return drink, dessert