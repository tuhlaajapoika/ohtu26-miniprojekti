import os
import shutil
import tempfile
import unittest
from types import SimpleNamespace

from app_library import AppLibrary
from refmanager.app import App
from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.exceptions import UserQuitException
from refmanager.models.reference_types import REFERENCE_TYPES
from stub_db import StubReferenceDatabase
from stub_io import StubIO


class TestApp(unittest.TestCase):
    def setUp(self):
        # For tests using AppLibrary
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        self._db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)

        # For tests using StubDB
        self._repository = StubReferenceDatabase()
        self.addCleanup(self._repository.close)
        self._io = StubIO()

        # "number: reference_type"
        self._ref_options = {
            str(number): reference_type
            for number, reference_type in enumerate(REFERENCE_TYPES.values(), start=1)
        }
        self._app = App(ref_repository=self._repository, io=self._io)

    def _ref_option_for(self, reference_type):
        """Returns number of the reference type"""
        return next(
            option
            for option, type_name in self._ref_options.items()
            if type_name == reference_type
        )

    def _assert_saved_reference_type(self, reference_type):
        row = (
            self._repository.get_db_connection()
            .execute('SELECT type FROM "references"')
            .fetchone()
        )
        self.assertEqual(row["type"], reference_type)

    # Tests using AppLibrary
    def test_new_reference_using_app_library(self):
        """Test new reference using AppLibrary"""
        app = AppLibrary(self._db_file)
        self.addCleanup(app.close)
        app.input(self._ref_option_for("Kirja"))
        app.input("Clean Code")
        app.input("Robert C. Martin")
        app.input("2008")
        app.input("Prentice hall")
        app.run_application("new")
        self.assertTrue(app.outputs()[-1].startswith("Viite lisätty (ID: "))

    # Tests using StubDB
    def test_running_command_new_adds_book_reference(self):
        self._io.inputs = [
            self._ref_option_for("Kirja"),
            "Testikirja",
            "Testitekijä",
            "2024",
            "Testikustantaja",
        ]
        self._app.run(command="new")
        self.assertIn("Viite lisätty", self._io.outputs[-1])
        self._assert_saved_reference_type("Kirja")

    def test_running_command_new_quits_when_zero_is_selected(self):
        self._io.inputs = ["0"]
        with self.assertRaisesRegex(UserQuitException, "Quitting the program."):
            self._app.run(command="new")

    def test_running_command_new_adds_article_referenve(self):
        self._io.inputs = [
            self._ref_option_for("Artikkeli"),
            "testiartikkeli",
            "Testitekijä",
            "2024",
            "12",
            "3",
            "45-50",
        ]
        self._app.run(command="new")
        self.assertIn("Viite lisätty", self._io.outputs[-1])
        self._assert_saved_reference_type("Artikkeli")

    def test_running_command_new_adds_webpage_reference(self):
        self._io.inputs = [
            self._ref_option_for("Verkkosivu"),
            "testisivu",
            "Testitekijä",
            "2024",
            "https://example.com",
            "21.20.2021",
        ]
        self._app.run(command="new")
        self.assertIn("Viite lisätty", self._io.outputs[-1])
        self._assert_saved_reference_type("Verkkosivu")

    def test_running_command_new_adds_conference_reference(self):
        self._io.inputs = [
            self._ref_option_for("Konferenssijulkaisu"),
            "testijulkaisu",
            "Testitekijä",
            "2024",
            "testikonferenssi",
        ]
        self._app.run(command="new")
        self.assertIn("Viite lisätty", self._io.outputs[-1])
        self._assert_saved_reference_type("Konferenssijulkaisu")

    def test_running_command_new_adds_thesis_reference(self):
        self._io.inputs = [
            self._ref_option_for("Opinnäytetyö tai väitöskirja"),
            "testityö",
            "Testitekijä",
            "2024",
            "testiyliopisto",
            "pro gradu",
        ]
        self._app.run(command="new")
        self.assertIn("Viite lisätty", self._io.outputs[-1])
        self._assert_saved_reference_type("Opinnäytetyö tai väitöskirja")

    def test_running_command_list_writes_references_from_repository(self):
        _reference = SimpleNamespace(
            ref_id=1,
            ref_type="Kirja",
            author="Martin",
            year=2008,
            title="Clean Code",
            publisher="Prentice Hall",
            tags="",
        )
        _repository = SimpleNamespace(find_all=lambda: [_reference])
        _app = App(ref_repository=_repository, io=self._io)
        _app.run(command="list")
        self.assertEqual(
            self._io.outputs, ["[Kirja]: Martin. Clean Code. Prentice Hall, 2008"]
        )

    def test_running_command_export_returns_not_implemented(self):
        self._app.run(command="export", export_path="test_references.bib")
        self.assertEqual(
            self._io.outputs, ["Not implemented: export -o test_references.bib"]
        )

    def test_running_command_new_with_invalid_reference_type(self):
        self._io.inputs = [
            str(len(self._ref_options) + 1),
            self._ref_option_for("Artikkeli"),
            "testiartikkeli",
            "2024",
            "22",
            "3",
            "38-40",
        ]
        self._app.run(command="new")
        self.assertIn(f"Virheellinen valinta.{os.linesep}", self._io.outputs)

    def test_running_command_new_saves_book_to_sqlite(self):
        _temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, _temp_dir)
        _db_file = os.path.join(_temp_dir, DATABASE_FILE_TESTS)
        _repository = SqliteReferenceRepository(_db_file)
        self.addCleanup(_repository.close)
        self._io.inputs = [
            self._ref_option_for("Kirja"),
            "Testikirja",
            "Testitekijä",
            "2024",
            "Testikustantaja",
        ]
        _app = App(ref_repository=_repository, io=self._io)
        _app.run(command="new")
        _row = (
            _repository.get_db_connection()
            .execute('SELECT title, type FROM "references"')
            .fetchone()
        )
        self.assertEqual(_row["title"], "Testikirja")
        self.assertEqual(_row["type"], "Kirja")

    # def test_export_command_writes_only_articles_to_a_bib_file(self):
    #    self._repository.save(
    #        ReferenceDTO(
    #            ref_id=uuid.uuid7(),
    #            ref_type="article",
    #            title="An article",
    #            author="A. Author",
    #            year=2025,
    #        )
    #    )
    #    self._repository.save(
    #        ReferenceDTO(
    #            ref_id=uuid.uuid7(),
    #            ref_type="book",
    #            title="A book",
    #            author="B. Author",
    #            year=2024,
    #        )
    #    )
    #    output_path = os.path.join(self._temp_dir, "articles.bib")
    #    self._app.run(command="export", export_path=output_path)
    #    with open(output_path, encoding="utf-8") as exported_file:
    #        bibtex = exported_file.read()
    #    self.assertIn("@article", bibtex)
    #    self.assertIn("An article", bibtex)
    #    self.assertNotIn("A book", bibtex)
    #    self.assertIn("Artikkeliviitteet viety tiedostoon", self._io.outputs[-1])
