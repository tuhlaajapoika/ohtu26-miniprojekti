import argparse

from refmanager.app import App
from refmanager.io.console_io import ConsoleIO


def main() -> None:
    """Function that prepares args, services and starts the main program."""
    parser = argparse.ArgumentParser(
        prog="refmanager",  # TODO: rename the program?
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
        help="Create a reference interactively",
        # description=("")
    )
    cmdparser.add_parser(
        "export",
        help="Export references to BibTex format",
        # description=("")
    )

    args = parser.parse_args()

    # Prepare and run
    db = False  # ReferencesDao()
    console_io = ConsoleIO()
    app = App(prog_args=args, refs_dao=db, io=console_io)
    app.run()


if __name__ == "__main__":
    main()
