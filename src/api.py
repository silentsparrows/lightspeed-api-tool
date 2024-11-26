import requests
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.category_utils import get_category_by_number
from src.console_utils import print_category_results, print_no_category_found, print_failed_request, print_filtered_domains

console = Console()

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

def filter_domains_by_category(links, category_names):
    """Filters domains based on one or more categories and prints matching domains in real-time."""
    filtered_domains = []
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_domain_filter, domain, category_names, filtered_domains): domain
            for domain in links
        }
        for future in as_completed(futures):
            future.result()

    if not filtered_domains:
        console.print("[bold red]No domains found under the specified categories.[/]")
    return filtered_domains

def process_domain_filter(domain, category_names, filtered_domains):
    """Handles the filtering for each domain with multiple categories."""
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
            if category_name_from_api and any(category_name_from_api.lower() == cat.lower() for cat in category_names):
                filtered_domains.append(domain)
                print_filtered_domains([domain], ", ".join(category_names))
