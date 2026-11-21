from refmanager.app import App
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from stub_io import StubIO

#not fully implemented yet
class AppLibrary:
    def __init__(self):
        self._io = StubIO()
        self._repository = SqliteReferenceRepository(db_file="references.db")
        # self._reference_service = ReferenceService
        self._app = App(ref_repository=self._repository, io=self._io)

    def input(self, value):
        self._io.add_input(value)

    def output_should_contain(self, value):
        outputs = self._io.outputs

        if not value in outputs:
            raise AssertionError(
                f'Output "{value}" is not in {outputs!s}'  # conversion flag str(outputs)
            )

    def run_application(self, command):
        self._app.run(command)

    def outputs(self):
        return self._io.outputs

    # def create_reference(self, title, author, year):
    #  self._reference_service.create(title, author, year)
