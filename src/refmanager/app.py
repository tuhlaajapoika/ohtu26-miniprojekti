from refmanager.services.reference_runner import ReferenceRunner


class App:
    """Application entry point that delegates commands to ReferenceRunner."""

    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io
        self.runner = ReferenceRunner(ref_repository, io)

    def run(self, command, export_path=None):
        """Starts the service"""
        if export_path is None:
            self.runner.run(command)
        else:
            self.runner.run(command, export_path=export_path)

    def quit(self):
        """Prepares the program for graceful exit"""
        self.repository.close()
