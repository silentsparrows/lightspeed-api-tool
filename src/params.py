import argparse
from src.api import query_domain_category, filter_domains_by_category
from src.file_utils import load_links_from_file
from src.console_utils import print_filtered_domains

def run_with_args(args):
    """Handles running the script with command-line arguments."""
    if args.bulk_cr:
        links = load_links_from_file('links.txt')
        if not links:
            return
        print(f"\nChecking categories for {len(links)} domains...\n")
        for domain in links:
            query_domain_category(domain)

    elif args.d:
        domain = args.d
        query_domain_category(domain)

    elif args.filter:
        category_name = args.filter
        links = load_links_from_file('links.txt')
        if not links:
            return
        print(f"\nFiltering domains under category '{category_name}'...\n")
        filtered_domains = filter_domains_by_category(links, category_name)
        print_filtered_domains(filtered_domains, category_name)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Domain Categorization Tool")

    parser.add_argument('--bulk-cr', action='store_true', help="Bulk query: Check categories for all domains in 'links.txt'")
    parser.add_argument('-d', '--d', type=str, help="Query a single domain (e.g., 'example.com')")
    parser.add_argument('-filter', type=str, help="Filter domains by category (e.g., 'security.proxy')")

    return parser.parse_args()
