from refmanager.services.reference_query import ReferenceRunner

class App:
    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io
        self.runner = ReferenceRunner(ref_repository, io)

    def run(self, command):
        self.runner.run(command)