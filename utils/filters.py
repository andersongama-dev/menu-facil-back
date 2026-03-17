def extract_exclusions(user_input):
    exclusions = []
    lower_input = user_input.lower()

    if "não quero" in lower_input:
        parts = lower_input.split("não quero")[1:]

        for p in parts:
            words = p.strip().split()
            if words:
                exclusions.append(" ".join(words[:2]))

    return exclusions


def filter_items_by_exclusion(items, exclusions):

    if not exclusions:
        return items

    filtered = []

    for item in items:
        name_desc = f"{item.name} {item.description}".lower()

        if not any(excl in name_desc for excl in exclusions):
            filtered.append(item)

    return filtered if filtered else items