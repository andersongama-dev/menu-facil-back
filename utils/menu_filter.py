def filter_menu(items, intent):
    filtered = []

    for item in items:
        desc = f"{item.name} {item.description}".lower()

        if any(ex.lower() in desc for ex in intent.get("exclude", [])):
            continue

        if any(inc.lower() not in desc for inc in intent.get("include", [])):
            continue

        filtered.append(item)

    return filtered