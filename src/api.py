import requests
from src.category_utils import get_category_by_number
from src.console_utils import print_category_results, print_no_category_found, print_failed_request, print_filtered_domains

url = "https://production-archive-proxy-api.lightspeedsystems.com/archiveproxy"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "x-api-key": "onEkoztnFpTi3VG7XQEq6skQWN3aFm3h"
}

def query_domain_category(domain):
    """Queries the category of a domain."""
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
        a_cat = formatResponse["data"]["a"]["cat"] if "a" in formatResponse["data"] else None

        if a_cat:
            category_name = get_category_by_number(a_cat)
            if category_name:
                print_category_results(domain, category_name)
            else:
                print_no_category_found(domain)
        else:
            print_no_category_found(domain)
    else:
        print_failed_request(domain, response.status_code)

def filter_domains_by_category(links, category_name):
    """Filters domains based on a specific category and prints matching domains in real-time."""
    filtered_domains = []  # This will store domains that match
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
            a_cat = formatResponse["data"]["a"]["cat"] if "a" in formatResponse["data"] else None

            if a_cat:
                category_name_from_api = get_category_by_number(a_cat)
                if category_name_from_api and category_name_from_api.lower() == category_name.lower():
                    filtered_domains.append(domain)
                    print_filtered_domains([domain], category_name)  # Print immediately when a match is found

    return filtered_domains