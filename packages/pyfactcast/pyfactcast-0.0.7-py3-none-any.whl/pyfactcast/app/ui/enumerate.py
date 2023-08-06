import typer
from rich.console import Console

import pyfactcast.app.business.enumerate as business

app = typer.Typer()
console = Console()


@app.command()
def namespaces() -> None:
    """
    List all available namespaces in alphabetical order.
    """
    for namespace in sorted(business.namespaces()):
        console.print(namespace, style="bold green")


@app.command()
def types(
    namespace: str = typer.Argument(..., help="A valid namespace you have access to")
) -> None:
    """
    List all types in a given namespace in alphabetical order
    """
    for type in sorted(business.types(namespace)):
        console.print(type, style="bold green")
