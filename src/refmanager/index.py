import argparse
import os
import sqlite3
import sys

from refmanager.app import App
from refmanager.config import DATABASE_FILE
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.io.console_io import ConsoleIO


def main() -> None:
    """Function that prepares args, services and starts the main program."""
    parser = argparse.ArgumentParser(
        prog="refmanager",
        description="Manage academic references with ease",
    )

    cmdparser = parser.add_subparsers(
        prog="refmanager", dest="command", metavar="COMMAND"
    )

    # With add_parser we can later define positional args for the commands.
    cmdparser.add_parser(
        "new",
        help="Create a new reference",
        description=(
            "Create new references interactively by filling required and optional fields"
        ),
    )
    cmdparser.add_parser(
        "list",
        help="List all references",
        description=("List all saved references in human readable format"),
    )
    cmdparser.add_parser(
        "export",
        help="Export references to BibTex format",
        description=("Export references to a .bib file in BibTex format"),
    )

    cmdparser.add_parser("quit", help="Quit the program")

    args = parser.parse_args()

    # When user does not give a command, print help
    if args.command is None:
        parser.print_help()
        return

    # Prepare and run
    console_io = ConsoleIO()
    try:
        sqlite_repository = SqliteReferenceRepository(db_file=DATABASE_FILE)
        app = App(ref_repository=sqlite_repository, io=console_io)
        try:
            app.run(command=args.command)
        except KeyboardInterrupt:
            print(f"{os.linesep}User interrupt captured.", console_io)
            sqlite_repository.close()
            sys.exit(130)
    except RuntimeError as e:
        print(f"ERROR: {e}")
    except sqlite3.OperationalError as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
