import os
import tempfile
import unittest
import shutil

from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.models.reference_dto import ReferenceDto


class TestSqliteReferenceRepository(unittest.TestCase):
    """Database tests for the SqliteReferenceRepository class."""

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        db_file = os.path.join(self._temp_dir, "references_test.db")
        self._repository = SqliteReferenceRepository(db_file)
        self.addCleanup(self._repository.close)

    def test_find_by_id_returns_none_when_reference_does_not_exist(self):
        self.assertIsNone(self._repository.find_by_id(22))

    def test_save_and_find_by_id(self):
        reference = ReferenceDto(
            ref_id=22,
            ref_type="article",
            title="Testing SQLite",
            author="Matti Meikäläinen",
            year=2026,
            publisher="",
        )
        self._repository.save(reference)
        self.assertEqual(self._repository.find_by_id(reference.ref_id), reference)

    def test_save_replaces_existing_reference_with_same_id(self):
        original = ReferenceDto(22, "article", "Original", "Keijo", 2020, "")
        updated = ReferenceDto(22, "book", "Updated", "Kaija", 2025, "FreshPublisher")
        self._repository.save(original)
        self._repository.save(updated)
        self.assertEqual(self._repository.find_by_id(updated.ref_id), updated)
