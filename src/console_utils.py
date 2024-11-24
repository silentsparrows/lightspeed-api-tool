from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_welcome():
    """Prints a welcome message to the console."""
    console.print(Panel("Lightspeed Categorization Tool", style="bold blue", width=40))

def print_category_results(domain, category_name):
    """Prints the categorization result."""
    console.print(f"[green]Domain:[/] {domain} [bold]Category:[/] {category_name}")

def print_no_category_found(domain):
    """Prints a message when no category is found."""
    console.print(f"[bold yellow]No category found for domain:[/] {domain}")

def print_failed_request(domain, status_code):
    """Prints a failure message if the request fails."""
    console.print(f"[bold red]Failed to fetch data for {domain}. Status code:[/] {status_code}")

def print_filtered_domains(filtered_domains, category_name):
    """Prints the list of filtered domains."""
    if filtered_domains:
        console.print(f"\n[bold green]Filtered Domains under '{category_name}':[/]")
        for domain in filtered_domains:
            console.print(f"- {domain}")
    else:
        console.print(f"\n[bold red]No domains found under the '{category_name}' category.")
