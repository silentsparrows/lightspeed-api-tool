from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from src.api import query_domain_category, filter_domains_by_category
from src.file_utils import load_links_from_file
from src.category_utils import get_category_by_number
from src.console_utils import print_welcome, print_category_results, print_filtered_domains

def main():
    console = Console()
    print_welcome()
    
    console.print("\n[bold]Choose an option:[/]")
    console.print("[1] Get categorization results from domain")
    console.print("[2] Filter out domains for a certain category")

    choice = Prompt.ask("Enter 1 or 2", choices=["1", "2"])

    if choice == "1":
        sub_choice = input("\n[bold]Choose how to provide domains:[/]\n[1] Enter a single domain\n[2] Provide domains in 'links.txt' for bulk query\n")

        if sub_choice == "1":
            domain = input("\nEnter a single domain to check: ")
            query_domain_category(domain)

        elif sub_choice == "2":
            links = load_links_from_file('links.txt')
            if not links:
                return
            print(f"\nChecking categories for {len(links)} domains...\n")
            for domain in links:
                query_domain_category(domain)

    elif choice == "2":
        category_name = input("\nEnter the category name to filter by (see ls.json for details): ")

        links = load_links_from_file('links.txt')
        if not links:
            return

        print(f"\nFiltering domains under category '{category_name}'...\n")
        filtered_domains = filter_domains_by_category(links, category_name)

        print_filtered_domains(filtered_domains, category_name)

    else:
        console.print("[bold red]Invalid option selected. Exiting.[/]")

    console.print("\n[bold cyan]Exiting program...[/]")

if __name__ == "__main__":
    main()
