import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

from src.categorization import query_domain_category
from src.filter import filter_domains_by_category
from src.file_utils import load_links_from_file

console = Console()


def main():
    console.print(
        Panel("Lightspeed Categorization Tool", style="bold blue", width=40))

    console.print("\n[bold]Choose an option:[/]")
    console.print("[1] Get categorization results from domain")
    console.print("[2] Filter out domains for a certain category")

    option = Prompt.ask("Enter 1 or 2", choices=["1", "2"])

    if option == "1":
        console.print("\n[bold]Choose how to provide domains:[/]")
        console.print("[A] Enter a single domain")
        console.print("[B] Provide domains in 'links.txt' for bulk query")

        sub_option = Prompt.ask("Enter a or b", choices=["a",
                                                         "b"]).strip().upper()

        if sub_option == "a":
            domain = Prompt.ask("\nEnter a single domain to check:")
            query_domain_category(domain)

        elif sub_option == "b":
            links = load_links_from_file('links.txt')
            if links is None:
                return  # exit
            console.print(
                f"\nChecking categories for the list of {len(links)} domains...\n"
            )
            for domain in links:
                query_domain_category(domain)

    elif option == "2":
        category_name = Prompt.ask(
            "\nEnter the category name to filter by:\n(see ls.json for list of categories)"
        )

        links = load_links_from_file('links.txt')
        if links is None:
            return

        console.print(
            f"\nFiltering domains under the category '{category_name}'...\n")
        filtered_domains = filter_domains_by_category(links, category_name)

        if filtered_domains:
            console.print(
                f"\n[bold green]Filtered Domains under '{category_name}':[/]")
            for domain in filtered_domains:
                console.print(f"- {domain}")
        else:
            console.print(
                f"\n[bold red]No domains found under the '{category_name}' category."
            )

    else:
        console.print("[bold red]Invalid option selected. Exiting.[/]")

    console.print("\n[bold cyan]Exiting program...[/]")


if __name__ == "__main__":
    main()
