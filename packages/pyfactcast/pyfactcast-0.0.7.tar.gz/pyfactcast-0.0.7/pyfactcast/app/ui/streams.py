from typing import Iterable, List
from uuid import UUID
import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
import json

import pyfactcast.app.business.streams as business

app = typer.Typer()
console = Console()


def print_iterable_as_json_list(
    iterable: Iterable,
) -> None:
    console.print("[")
    it = iter(iterable)

    try:
        last = next(it)  # type: ignore
    except StopIteration:
        console.print("]")
        return

    for elem in it:
        console.print(f"{last.json(indent=2)},", soft_wrap=True)
        last = elem
    console.print(last.json(indent=2), soft_wrap=True)
    console.print("]")


@app.command()
def subscribe(
    namespace: str,
    follow: bool = typer.Option(
        False, "--follow", help="Stay connected and listen for new events."
    ),
    from_now: bool = typer.Option(
        False, "--from-now", help="Follow the event stream starting now."
    ),
    after_fact: UUID = typer.Option(
        None, help="Get all events in the stream that happened after a certain ID."
    ),
    json_format: bool = typer.Option(False, "--json", help="Output raw json events."),
    fact_types: List[str] = typer.Option(
        [],
        "--type",
        help="The types of events to get. Can be used multiple times. Supports regexp.",
    ),
    type_versions: List[int] = typer.Option(
        [],
        "--version",
        help="The versions of the types to get. Will be right padded with latest. If used regex for types is not supported.",
    ),
) -> None:
    """
    Subscribe to an eventstream.

    You can select types you want to subscribe to. When doing so you can also use regexes to subscribe to multiple
    event types in short order for example ``... subscribe machinery --type Assembly.*``
    will get you all Assembly events for example AssemblyCreated, AssemblyCompleted, AssemblyDestroyed but nothing related
    to Subassemblies. If you specify no types, all types will be streamed.

    You can also get event types in specific versions.
    You can either specify them intermixed with the types like this
    ``... subscribe machinery --type AssemblyCreated --version 1 --type AssemblyUsed --version 3``
    or you can write them out after each other like this
    ``... subscribe machinery --type AssemblyCreated --type AssemblyUsed --version 1 --version 3``.
    In both cases you will get version 1 of AssemblyCreated and version 3 of AssemblyUsed.
    You can specify fewer versions than types. In this case matching will be left to right by postion in the list.
    Types without a version will give you the latest version. This leads to a slightly strange case where
    ``... subscribe machinery --type AssemblyCreated --type AssemblyUsed --version 2``
    will give you version 2 of AssemblyCreated and the latest version of AssemblyUsed.
    It is recommended to put the types you need the latest version of last and use intermixed notation before that.
    If you want to explicitly specify the latest version, please specify ``--version 0``


    To keep other complexities out of this, if you use versions you will not be able
    to use regexes. This is mostly due to the ambiguities that come along when you specify something like this
    ``... subscribe machinery --type Assembly.* --version 2`` do you want version 2 of everything or version 2 of the first match
    and latest of everything else?
    """
    subscription = business.subscribe(
        namespace=namespace,
        follow=follow,
        after_fact=after_fact,
        from_now=from_now,
        fact_types=fact_types,
        type_versions=type_versions,
    )

    if json_format:
        print_iterable_as_json_list(subscription)
        return

    for elem in subscription:
        table = Table(show_header=False, show_lines=True, header_style="bold magenta")
        table.add_column("Time")
        table.add_column("Type")
        table.add_column("Header")
        table.add_column("Payload")
        table.add_row(
            datetime.fromtimestamp(int(elem.header.meta["_ts"][:10])).isoformat(),  # type: ignore
            elem.header.type,
            elem.header.json(indent=2),
            json.dumps(elem.payload, indent=2),
        )
        console.print(table)
