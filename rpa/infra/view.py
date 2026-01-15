from rich.console import Console
from rich.text import Text

console = Console()


def show_product(item: dict):
    text = Text()
    text.append(item["name"], style="bold white")
    text.append(" | ", style="dim")
    text.append(item["barcode"], style="cyan")
    text.append(" | qty=", style="dim")
    text.append(str(item["quantity"]), style="yellow")
    text.append(" | price=", style="dim")
    text.append(str(item["price"]), style="green")
    text.append(" | wholesale=", style="dim")
    text.append(str(item["wholesale_price"]), style="green")
    text.append(" (min ", style="dim")
    text.append(str(item["wholesale_minimum_quantity"]), style="yellow")
    text.append(")", style="dim")

    console.print(text)

def show_field(field: str):
    console.print(f"  • {field}", style="white")

def show_success():
    console.print("  ✓ cadastrado\n", style="bold green")

def show_error(error: str):
    console.print(f"  ✗ erro: {error}\n", style="bold red")


