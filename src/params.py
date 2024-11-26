import argparse
from src.api import query_domain_category, filter_domains_by_category
from src.file_utils import load_links_from_file
from concurrent.futures import ThreadPoolExecutor

def run_with_args(args):
    """Handles running the script with command-line arguments."""
    if args.bulk_cr:
        links = load_links_from_file('links.txt')
        if not links:
            return
        print(f"\nChecking categories for {len(links)} domains...\n")

        # Using threadpoolexecutor to run query_domain_category concurrently
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(query_domain_category, domain): domain for domain in links}
            for future in futures:
                future.result()

    elif args.d:
        domain = args.d
        query_domain_category(domain)

    elif args.filter:
        category_input = args.filter
        categories = [cat.strip() for cat in category_input.split(",")]

        links = load_links_from_file('links.txt')
        if not links:
            return

        print(f"\nFiltering domains under categories: {', '.join(categories)}...\n")

        # PRint live rather than having it do it at the end
        filter_domains_by_category(links, categories)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Domain Categorization Tool")

    parser.add_argument('--bulk-cr', action='store_true', help="Bulk query: Check categories for all domains in 'links.txt'")
    parser.add_argument('-d', '--d', type=str, help="Query a single domain (e.g., 'example.com')")
    parser.add_argument('-filter', '--filter', type=str, help="Filter domains by categories (comma-separated, NO SPACES, e.g., 'general,computers')")

    return parser.parse_args()
