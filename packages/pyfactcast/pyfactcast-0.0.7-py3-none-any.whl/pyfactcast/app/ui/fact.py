from uuid import UUID
import typer
from rich.console import Console

import pyfactcast.app.business.fact as business

app = typer.Typer()
console = Console()


@app.command()
def serial_of(fact_id: UUID) -> None:
    """
    Returns the serial for the fact identified by the given UUID
    """
    serial = business.serial_of(fact_id)
    if serial:  # 3.8 Walrus
        console.print(serial)
    else:
        console.print(f"No fact with id {fact_id} found.")
