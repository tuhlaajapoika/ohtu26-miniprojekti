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

    # Tag ----------------------------------------------------------------------
    tag_parser = argparse.ArgumentParser(add_help=False)
    tag_parser.add_argument(
        "-t",
        "--tag",
        nargs="+",
        help="Specify one or more tags",
    )

    # New ----------------------------------------------------------------------
    cmdparser.add_parser(
        "new",
        help="Create a new reference",
        description=(
            "Create new references interactively by filling required and optional fields"
        ),
        parents=[tag_parser],
    )

    # List ---------------------------------------------------------------------
    cmdparser.add_parser(
        "list",
        help="List all references",
        description="List all saved references in human readable format",
        parents=[tag_parser],
    )

    # Export -------------------------------------------------------------------
    cmdparser.add_parser(
        "export",
        help="Export references to BibTex format",
        description="Export references to a .bib file in BibTex format",
        parents=[tag_parser],
    )

    # Quit ---------------------------------------------------------------------
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
            console_io.write(f"{os.linesep}User interrupt captured.")
            app.quit()
            sys.exit(130)
    except RuntimeError as e:
        console_io.write(f"ERROR: {e}")
        sys.exit(1)
    except sqlite3.OperationalError as e:
        console_io.write(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
