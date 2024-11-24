import json

def get_category_by_number(category_number):
    """Fetches category data from the ls.json file."""
    try:
        with open('ls.json', 'r') as file:
            ls_cat = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[bold red]Error:[/] 'ls.json' cannot be read.")
        return None

    if isinstance(ls_cat, list):
        for item in ls_cat:
            if item.get("CategoryNumber") == category_number:
                return item['CategoryName']
    return None
