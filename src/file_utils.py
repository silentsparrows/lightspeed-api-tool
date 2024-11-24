def load_links_from_file(filename):
    """Loads the list of domains from a text file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {filename} cannot be read or does not exist.")
        return None
