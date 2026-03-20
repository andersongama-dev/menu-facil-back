from utils.items import fetch_all_menu_items
import unicodedata

menu_items = fetch_all_menu_items()

combo_rules = {
    "pizza": ["vinho", "sobremesa"],
    "hamburguer": ["batata frita", "coca"],
    "sobremesa": ["suco natural"],
}

def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

def combo_suggest(item_name: str):
    item_name_norm = normalize(item_name)

    if "pizza" in item_name_norm:
        accomp_types = combo_rules["pizza"]
        message = "Sugestão de combo para pizza:"
    elif "hamburguer" in item_name_norm:
        accomp_types = combo_rules["hamburguer"]
        message = "Sugestão de combo para hambúrguer:"
    elif "sobremesa" in item_name_norm:
        accomp_types = combo_rules["sobremesa"]
        message = "Sugestão de combo para sobremesa:"
    else:
        return {"items": [], "message": "Não há sugestão de combo para este item."}

    suggestions = [
        item for item in menu_items
        if any(acc in normalize(item.name) for acc in accomp_types)
    ]

    if not suggestions:
        return {"items": [], "message": f"Não há combos sugeridos para {item_name}."}

    return {"items": suggestions, "message": message}