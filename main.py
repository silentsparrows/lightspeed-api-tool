from rich.console import Console
from rich.prompt import Prompt
from src.api import query_domain_category, filter_domains_by_category
from src.file_utils import load_links_from_file
from src.console_utils import print_welcome, print_filtered_domains
from src.params import parse_arguments, run_with_args
from concurrent.futures import ThreadPoolExecutor

def main():
    console = Console()

    try:
        args = parse_arguments()

        if args.bulk_cr or args.d or args.filter:
            run_with_args(args)
        else:
            # run CLI if no args provided
            print_welcome()
            console.print("\n[bold]Choose an option:[/]")
            console.print("[1] Get categorization results from domain")
            console.print("[2] Filter out domains for a certain category")

            choice = Prompt.ask("Enter 1 or 2", choices=["1", "2"])

            if choice == "1":
                console.print("\n[bold]Choose how to provide domains:[/]")
                console.print("[1] Enter a single domain")
                console.print("[2] Provide domains in 'links.txt' for bulk query")
                sub_choice = Prompt.ask("Enter 1 or 2", choices=["1", "2"]).strip().upper()

                if sub_choice == "1":
                    domain = Prompt.ask("\nEnter a single domain to check")
                    query_domain_category(domain)

                elif sub_choice == "2":
                    links = load_links_from_file('links.txt')
                    if not links:
                        return
                    print(f"\nChecking categories for {len(links)} domains...\n")
                    with ThreadPoolExecutor() as executor:
                        # "Submit tasks for querying all domains concurrently" stack overflow
                        futures = [executor.submit(query_domain_category, domain) for domain in links]
                        for future in futures:
                            future.result()  # wait until all of the futures are done

            elif choice == "2":
                category_name = input("\nEnter the category name to filter by (see ls.json for details): ")

                links = load_links_from_file('links.txt')
                if not links:
                    return

                print(f"\nFiltering domains under category '{category_name}'...\n")
                filtered_domains = filter_domains_by_category(links, category_name)

                # The real-time printing will already be handled by the filter function
                # If no domains were found, print the final message
                if not filtered_domains:
                    print_filtered_domains([], category_name)

            else:
                console.print("[bold red]Invalid option selected. Exiting.[/]")

    except KeyboardInterrupt:
        console.print("\n[bold cyan]Exiting program...[/]")

if __name__ == "__main__":
    main()
