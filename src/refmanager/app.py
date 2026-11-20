import sys


class App:
    """A class that represents the main application for managing references."""

    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io

    def run(self, command):
        try:
            match command:
                case "new":
                    self.io.write("Not implemented: new")
                case "list":
                    self.io.write("Not implemented: list")
                case "export":
                    self.io.write("Not implemented: export")
        except RuntimeError as e:
            self.io.write(f"{e}")
            sys.exit(1)
