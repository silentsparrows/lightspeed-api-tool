from src.api import filter_domains_by_category

def filter_domains_by_category_name(links, category_name):
    """Filters domains based on a specific category."""
    filtered_domains = filter_domains_by_category(links, category_name)
    return filtered_domains
