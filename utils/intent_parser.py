def parse_user_intent(text: str):

    text = text.lower()

    restrictions = []
    include = []
    exclude = []

    if "vegetariano" in text:
        restrictions.append("vegetariano")

    if "vegano" in text:
        restrictions.append("vegano")

    if "sem tomate" in text:
        exclude.append("tomate")

    if "frango" in text:
        include.append("frango")

    return {
        "include": include,
        "exclude": exclude,
        "restrictions": restrictions
    }