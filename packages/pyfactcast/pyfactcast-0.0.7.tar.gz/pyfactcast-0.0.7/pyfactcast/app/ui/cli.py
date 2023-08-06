import typer
from rich.console import Console
import logging
from rich.logging import RichHandler

from .enumerate import app as enum_app
from .streams import app as sub_app
from .fact import app as fac_app


console = Console()
app = typer.Typer()

FORMAT = "%(message)s"


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Put out more details on the event stream meta events.",
    )
):
    level = "WARNING"
    if verbose:
        level = "DEBUG"

    logging.basicConfig(
        level=level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )


app.add_typer(enum_app, name="enumerate")
app.add_typer(sub_app, name="streams")
app.add_typer(fac_app, name="fact")


typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()
