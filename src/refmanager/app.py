from refmanager.services.reference_query import ReferenceRunner


class App:
    """Application entry point that delegates commands to ReferenceRunner."""

    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io
        self.runner = ReferenceRunner(ref_repository, io)

    def run(self, command):
        """Starts service runner

        Args:
            command (dynamic attribute): command passed into the program by the user
        """
        self.runner.run(command)

    def quit(self):
        """Closes the repository"""
        self.repository.close()
