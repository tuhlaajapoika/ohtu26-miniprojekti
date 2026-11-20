import sys


class App:
    """Object that operates on user's commands"""

    def __init__(self, prog_args, refs_dao, io):
        self.args = prog_args
        self.db = refs_dao
        self.io = io

    def run(self):
        try:
            match self.args.command:
                case "new":
                    print("Not implemented: new")
                case "list":
                    print("Not implemented: list")
                case "export":
                    print("Not implemented: export")
        except RuntimeError as e:
            print(f"ERROR: {e}", self.io)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nUser interrupt captured.", self.io)
            sys.exit(130)
