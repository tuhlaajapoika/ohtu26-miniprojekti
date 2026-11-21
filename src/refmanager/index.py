import argparse
import sys

from refmanager.app import App
from refmanager.config import DATABASE_FILE
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.io.console_io import ConsoleIO

def main()->None:
    """Function that prepares args, services and starts the main program."""
    parser = argparse.ArgumentParser(
        prog="refmanager",# rename the program?
        description="Manage academic references with ease",
    )

    # Set as mandatory argument.
    cmdparser = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="COMMAND",
    )

    # With add_parser we can later define positional args for the commands.
    cmdparser.add_parser(
        "new",
        help="Create a reference interactively",
        # description=("")
    )
    cmdparser.add_parser(
        "list",
        help="List all references",
        # description=("")
    )
    cmdparser.add_parser(
        "export",
        help="Export references to BibTex format",
        # description=("")
    )

    args = parser.parse_args()

    # Prepare and run
    console_io = ConsoleIO()
    # try:
    sqlite_repository = SqliteReferenceRepository(db_file=DATABASE_FILE)
    app = App(ref_repository=sqlite_repository, io=console_io)
    try:
        app.run(command=args.command)
    except KeyboardInterrupt:
        print("\nUser interrupt captured.", console_io)
        conn = sqlite_repository.get_db_connection()
        conn.close()
        sys.exit(130)
    # except Exception as e:
    #    print(f"{e}", console_io)


if __name__ == "__main__":
    main()
