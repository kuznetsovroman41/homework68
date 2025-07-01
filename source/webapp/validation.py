def validate(data):
    errors = {}
    title = data.get('title')

    if not title:
        errors["title"] = "This field is required."
    elif len(title) < 3:
        errors["title"] = "Title must be at least 3 characters long."

    return errors