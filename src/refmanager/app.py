from refmanager.services.reference_query import ReferenceRunner


class App:  # pylint: disable=too-few-public-methods
    """Application entry point that delegates commands to ReferenceRunner."""

    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io
        self.runner = ReferenceRunner(ref_repository, io)

    def run(self, command):
        self.runner.run(command)
