import unittest

from refmanager.app import App
from stub_db import StubReferenceDatabase
from stub_io import StubIO


class TestApp(unittest.TestCase):
    def setUp(self):
        self._repository = StubReferenceDatabase()
        self.addCleanup(self._repository.cleanup)
        self._io = StubIO()
        self._app = App(ref_repository=self._repository, io=self._io)

    def test_running_command_new_returns_not_implemented(self):
        self._app.run(command="new")
        self.assertEqual(self._io.outputs, ["Not implemented: new"])

    def test_running_command_list_returns_not_implemented(self):
        self._app.run(command="list")
        self.assertEqual(self._io.outputs, ["Not implemented: list"])

    def test_running_command_export_returns_not_implemented(self):
        self._app.run(command="export")
        self.assertEqual(self._io.outputs, ["Not implemented: export"])
