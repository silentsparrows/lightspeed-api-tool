import requests
from src.query import get_category_by_number

url = "https://production-archive-proxy-api.lightspeedsystems.com/archiveproxy"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua":
    "\"Chromium\";v=\"130\", \"Brave\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
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
        a_cat = formatResponse["data"]["a"]["cat"] if "a" in formatResponse[
            "data"] else None

        if a_cat:
            category_name = get_category_by_number(a_cat)
            if category_name:
                print(f"Domain: {domain} - Category: {category_name}")
            else:
                print(f"No category found for domain: {domain}")
        else:
            print(f"No category data available for domain: {domain}")
    else:
        print(f"Failed to fetch data for {domain}. Status code: {response.status_code}")
