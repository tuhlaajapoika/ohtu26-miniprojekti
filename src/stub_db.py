import os
import shutil
import sqlite3
import tempfile
import uuid

from refmanager.config import DATABASE_FILE_TESTS
from refmanager.db.initialize_database import initialize_database


class StubReferenceDatabase:
    """
    A stub implementation of a reference database for testing purposes.

    Uses temporary directory for the database file.
    """

    def __init__(self, _db_file=DATABASE_FILE_TESTS):
        self._temp_dir = tempfile.mkdtemp()
        self._test_db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)
        self._conn = sqlite3.connect(self._test_db_file)
        self._conn.row_factory = sqlite3.Row
        initialize_database(self._conn)

    def get_db_connection(self):
        return self._conn

    def close(self):
        self._conn.commit()
        self._conn.close()
        shutil.rmtree(self._temp_dir)

    def save(self, ref):
        if ref.ref_id is None:
            ref.ref_id = uuid.uuid7()
        self._conn.execute(
            """
            INSERT OR REPLACE INTO "references"
                (reference_id, type, title, author, year, publisher)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                str(ref.ref_id),
                ref.ref_type,
                ref.title,
                ref.author,
                ref.year,
                ref.publisher,
            ),
        )
        self._conn.commit()
