import requests
from src.query import get_category_by_number


def filter_domains_by_category(links, category_name):
    """Filters domains based on a specific category."""
    filtered_domains = []

    for domain in links:
        body = {
            "query": """
                query getDeviceCategorization($itemA: CustomHostLookupInput!){
                  a: custom_HostLookup(item: $itemA) {
                    cat
                  }
                }
            """,
            "variables": {
                "itemA": {
                    "hostname": domain,
                    "getArchive": True
                }
            }
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            formatResponse = response.json()
            a_cat = formatResponse["data"]["a"][
                "cat"] if "a" in formatResponse["data"] else None

            if a_cat:
                category_name_from_api = get_category_by_number(a_cat)
                if category_name_from_api and category_name_from_api.lower(
                ) == category_name.lower():
                    filtered_domains.append(domain)

    return filtered_domains
