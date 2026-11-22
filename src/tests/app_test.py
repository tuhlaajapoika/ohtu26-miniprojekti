import os
import tempfile
import unittest
from types import SimpleNamespace

from refmanager.app import App
from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from stub_db import StubReferenceDatabase
from stub_io import StubIO


class TestApp(unittest.TestCase):
    def setUp(self):
        self._repository = StubReferenceDatabase()
        self.addCleanup(self._repository.cleanup)
        self._io = StubIO()
        self._app = App(ref_repository=self._repository, io=self._io)

    def test_running_command_new_adds_book_reference(self):
        self._io.inputs = ["1", "Testikirja", "Testitekijä", "2024", "Testikustantaja"]
        self._app.run(command="new")
        self.assertEqual(len(self._io.outputs), 2)
        self.assertIn("Viite lisätty", self._io.outputs[-1])

    def test_running_command_new_adds_article_referenve(self):
        self._io.inputs = [
            "2",
            "testiartikkeli",
            "Testitekijä",
            "2024",
            "12",
            "3",
            "45-50",
        ]
        self._app.run(command="new")
        self.assertEqual(len(self._io.outputs), 2)
        self.assertIn("Viite lisätty", self._io.outputs[-1])

    def test_running_command_new_adds_webpage_reference(self):
        self._io.inputs = [
            "3",
            "testisivu",
            "Testitekijä",
            "2024",
            "https://example.com",
            "21.20.2021",
        ]
        self._app.run(command="new")
        self.assertEqual(len(self._io.outputs), 2)
        self.assertIn("Viite lisätty", self._io.outputs[-1])

    def test_running_command_new_adds_conference_reference(self):
        self._io.inputs = [
            "4",
            "testijulkaisu",
            "Testitekijä",
            "2024",
            "testikonferenssi",
        ]
        self._app.run(command="new")
        self.assertEqual(len(self._io.outputs), 2)
        self.assertIn("Viite lisätty", self._io.outputs[-1])

    def test_running_command_new_adds_thesis_reference(self):
        self._io.inputs = [
            "5",
            "testityö",
            "Testitekijä",
            "2024",
            "testiyliopisto",
            "pro gradu",
        ]
        self._app.run(command="new")
        self.assertEqual(len(self._io.outputs), 2)
        self.assertIn("Viite lisätty", self._io.outputs[-1])

    def test_running_command_list_writes_references_from_repository(self):
        reference = SimpleNamespace(
            ref_id=1, author="Martin", year=2008, title="Clean Code"
        )
        repository = SimpleNamespace(find_all=lambda: [reference])
        app = App(ref_repository=repository, io=self._io)

        app.run(command="list")

        self.assertEqual(self._io.outputs, ["[1] Martin (2008): Clean Code"])

    def test_running_command_export_returns_not_implemented(self):
        self._app.run(command="export")
        self.assertEqual(self._io.outputs, ["Not implemented: export"])

    def test_running_command_new_with_invalid_reference_type(self):
        self._io.inputs = ["9", "2", "testiartikkeli", "2024", "22", "3", "38-40"]
        self._app.run(command="new")

        self.assertIn(
            "Virheellinen valinta. Valitse 1, 2, 3, 4 tai 5. ", self._io.outputs
        )

    def test_running_command_new_saves_book_to_sqlite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_file = os.path.join(temp_dir, DATABASE_FILE_TESTS)
            repository = SqliteReferenceRepository(db_file)
            self.addCleanup(repository.get_db_connection().close)

            io = StubIO()

            io.inputs = ["1", "Testikirja", "Testitekijä", "2024", "Testikustantaja"]
            app = App(ref_repository=repository, io=io)
            app.run(command="new")

            row = (
                repository.get_db_connection()
                .execute('SELECT title FROM "references"')
                .fetchone()
            )

            self.assertEqual(row["title"], "Testikirja")
