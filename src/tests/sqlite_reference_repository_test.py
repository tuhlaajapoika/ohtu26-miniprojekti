import os
import shutil
import tempfile
import unittest
import uuid

from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.models.reference_dto import ReferenceDto


class TestSqliteReferenceRepository(unittest.TestCase):
    """Database tests for the SqliteReferenceRepository class."""

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)
        self._repository = SqliteReferenceRepository(db_file)
        self.addCleanup(self._repository.close)

    def test_find_by_id_returns_none_when_reference_does_not_exist(self):
        self.assertIsNone(self._repository.find_by_id(uuid.uuid7()))

    def test_id_creation_when_a_reference_is_created_but_id_is_empty(self):
        reference = ReferenceDto(
            ref_id=None,
            ref_type="article",
            title="Testing SQLite",
            author="Matti Meikäläinen",
            year=2026,
            publisher="",
        )
        self._repository.save(reference)
        _ref_list = self._repository.find_all()
        self.assertIsNotNone(_ref_list[0])
        ref_id = _ref_list[0].ref_id
        assert ref_id is not None
        found_reference = self._repository.find_by_id(ref_id)
        assert found_reference is not None
        self.assertEqual(found_reference.title, reference.title)

    def test_save_and_find_by_id(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDto(
            ref_id=ref_id,
            ref_type="article",
            title="Testing SQLite",
            author="Matti Meikäläinen",
            year=2026,
            publisher="",
        )
        self._repository.save(reference)
        self.assertEqual(self._repository.find_by_id(ref_id), reference)

    def test_save_replaces_existing_reference_with_same_id(self):
        ref_id = uuid.uuid7()
        original = ReferenceDto(ref_id, "article", "Original", "Keijo", 2020, "")
        updated = ReferenceDto(
            ref_id, "book", "Updated", "Kaija", 2025, "FreshPublisher"
        )
        self._repository.save(original)
        self._repository.save(updated)
        self.assertEqual(self._repository.find_by_id(ref_id), updated)

    def test_find_all_returns_empty_list_when_no_references(self):
        self.assertEqual(self._repository.find_all(), [])

    def test_find_all_returns_all_saved_references(self):
        first = ReferenceDto(
            uuid.uuid7(),
            "book",
            "Clean Code",
            "Robert C. Martin",
            2008,
            "Prentice Hall",
        )
        second = ReferenceDto(
            uuid.uuid7(), "article", "Testing SQLite", "Matti Meikäläinen", 2026, ""
        )
        self._repository.save(first)
        self._repository.save(second)
        self.assertCountEqual(self._repository.find_all(), [first, second])
