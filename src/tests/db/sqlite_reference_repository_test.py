import os
import shutil
import sqlite3
import tempfile
import unittest
import uuid
from unittest.mock import Mock, patch

from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.models.reference_dto import ReferenceDTO


class TestSqliteReferenceRepository(unittest.TestCase):
    """Database tests for the SqliteReferenceRepository class."""

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        self._db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)
        self._repository = SqliteReferenceRepository(self._db_file)
        self.addCleanup(self._repository.close)

    def test_find_by_id_returns_none_when_reference_does_not_exist(self):
        self.assertIsNone(self._repository.find_by_id(uuid.uuid7()))

    def test_save_and_find_by_id(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDTO(
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
        original = ReferenceDTO(ref_id, "article", "Original", "Keijo", 2020, "")
        updated = ReferenceDTO(
            ref_id, "book", "Updated", "Kaija", 2025, "FreshPublisher"
        )
        self._repository.save(original)
        self._repository.save(updated)
        self.assertEqual(self._repository.find_by_id(ref_id), updated)

    def test_find_all_returns_empty_list_when_no_references(self):
        self.assertEqual(self._repository.find_all(), [])

    def test_find_all_returns_all_saved_references(self):
        first = ReferenceDTO(
            uuid.uuid7(),
            "book",
            "Clean Code",
            "Robert C. Martin",
            2008,
            "Prentice Hall",
        )
        second = ReferenceDTO(
            uuid.uuid7(), "article", "Testing SQLite", "Matti Meikäläinen", 2026, ""
        )
        self._repository.save(first)
        self._repository.save(second)
        self.assertCountEqual(self._repository.find_all(), [first, second])

    def test_delete_removes_reference_by_id(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDTO(
            ref_id,
            "article",
            "Testing SQLite",
            "Esimerkki Erkki",
            2026,
            "",
        )
        other_reference = ReferenceDTO(
            uuid.uuid7(),
            "book",
            "Clean Code",
            "Robert C. Martin",
            2008,
            "Prentice Hall",
        )

        self._repository.save(reference)
        self._repository.save(other_reference)

        self._repository.delete(ref_id)

        self.assertIsNone(self._repository.find_by_id(ref_id))
        self.assertEqual(
            self._repository.find_by_id(other_reference.ref_id),
            other_reference,
        )

    def test_delete_raises_error_when_reference_does_no_exist(self):
        ref_id = uuid.uuid7()

        with self.assertRaises(RuntimeError):
            self._repository.delete(ref_id)

    def test_tags_are_saved_and_loaded(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDTO(
            ref_id,
            "book",
            "Clean Code",
            "Robert C. Martin",
            2008,
            "Prentice Hall",
            tags="koodi,ohjelmointi",
        )
        self._repository.save(reference)
        found = self._repository.find_by_id(ref_id)
        assert found is not None
        self.assertEqual(found.tags, "koodi,ohjelmointi")

    # Failure and rollback operations tests

    def test_database_connection_failure(self):
        with (
            patch(
                "refmanager.db.sqlite_reference_repository.sqlite3.connect",
                side_effect=sqlite3.OperationalError("unable to open database"),
            ),
            self.assertRaises(sqlite3.OperationalError),
        ):
            _test_repository = SqliteReferenceRepository(self._db_file)

    def test_find_all_closing_cursor_when_query_fails(self):
        cursor = Mock()
        cursor.execute.side_effect = sqlite3.OperationalError("injected failure")
        connection = Mock()
        connection.cursor.return_value = cursor

        with (
            patch.object(self._repository, "conn", connection),
            self.assertRaises(sqlite3.OperationalError),
        ):
            self._repository.find_all()

        cursor.close.assert_called_once()

    def test_database_rollback_on_failed_save_operation(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDTO(ref_id, "article", "Title", "Author", 2026, "")

        self._repository.conn.execute("CREATE TABLE rollback_probe (reference_id TEXT)")
        # The trigger runs after a row is inserted into "references" table.
        self._repository.conn.execute("""
            CREATE TRIGGER fail_after_insert
            AFTER INSERT ON "references"
            BEGIN
                INSERT INTO rollback_probe VALUES (NEW.reference_id);
                SELECT RAISE(FAIL, 'injected failure');
            END;
        """)

        with self.assertRaises(sqlite3.IntegrityError):
            self._repository.save(reference)

        self.assertIsNone(self._repository.find_by_id(ref_id))
        self.assertEqual(
            self._repository.conn.execute(
                "SELECT reference_id FROM rollback_probe"
            ).fetchall(),
            [],
        )

    def test_database_rollback_on_failed_delete_operation(self):
        ref_id = uuid.uuid7()
        reference = ReferenceDTO(ref_id, "article", "Title", "Author", 2026, "")
        self._repository.conn.execute("CREATE TABLE rollback_probe (reference_id TEXT)")
        self._repository.save(reference)
        # The trigger runs after a row is deleted from "references".
        self._repository.conn.execute("""
            CREATE TRIGGER fail_after_delete
            AFTER DELETE ON "references"
            BEGIN
                INSERT INTO rollback_probe VALUES (OLD.reference_id);
                SELECT RAISE(FAIL, 'injected failure');
            END;
        """)

        with self.assertRaises(sqlite3.IntegrityError):
            self._repository.delete(ref_id)

        found_reference = self._repository.find_by_id(ref_id)
        self.assertEqual(found_reference, reference)
        self.assertEqual(
            self._repository.conn.execute(
                "SELECT reference_id FROM rollback_probe"
            ).fetchall(),
            [],
        )
