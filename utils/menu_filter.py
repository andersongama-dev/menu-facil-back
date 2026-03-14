def filter_menu(items, intent):

    filtered = []

    for item in items:

        desc = (item.name + " " + item.description).lower()

        valid = True

        for ex in intent["exclude"]:
            if ex in desc:
                valid = False

        for inc in intent["include"]:
            if inc not in desc:
                valid = False

        if valid:
            filtered.append(item)

    return filtered