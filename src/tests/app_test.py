import os
import shutil
import tempfile
import unittest
from types import SimpleNamespace

from app_library import AppLibrary
from refmanager.app import App
from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from stub_db import StubReferenceDatabase
from stub_io import StubIO


class TestApp(unittest.TestCase):
    def setUp(self):
        # AppLibrary
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        self._db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)
        # StubDB
        self._repository = StubReferenceDatabase()
        self.addCleanup(self._repository.close)
        self._io = StubIO()
        self._app = App(ref_repository=self._repository, io=self._io)

    # Tests using AppLibrary
    def test_new_reference_using_app_library(self):
        """Test new reference using AppLibrary"""
        app = AppLibrary(self._db_file)
        self.addCleanup(app.close)
        app.input("1")
        app.input("Clean Code")
        app.input("Robert C. Martin")
        app.input("2008")
        app.input("Prentice hall")
        app.run_application("new")
        self.assertTrue(app.outputs()[-1].startswith("Viite lisätty (ID: "))

    # Tests using StubDB
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
        _reference = SimpleNamespace(
            ref_id=1,
            ref_type="Kirja",
            author="Martin",
            year=2008,
            title="Clean Code",
            publisher="Prentice Hall",
        )
        _repository = SimpleNamespace(find_all=lambda: [_reference])
        _app = App(ref_repository=_repository, io=self._io)
        _app.run(command="list")
        self.assertEqual(
            self._io.outputs, ["[Kirja]: Martin. Clean Code. Prentice Hall, 2008"]
        )

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
        _temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, _temp_dir)
        _db_file = os.path.join(_temp_dir, DATABASE_FILE_TESTS)
        _repository = SqliteReferenceRepository(_db_file)
        self.addCleanup(_repository.close)
        self._io.inputs = [
            "1",
            "Testikirja",
            "Testitekijä",
            "2024",
            "Testikustantaja",
        ]
        _app = App(ref_repository=_repository, io=self._io)
        _app.run(command="new")
        _row = (
            _repository.get_db_connection()
            .execute('SELECT title FROM "references"')
            .fetchone()
        )
        self.assertEqual(_row["title"], "Testikirja")
