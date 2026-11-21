import os
import sqlite3

from refmanager.db.initialize_database import initialize_database


class StubReferenceDatabase:
    """A stub implementation of a reference database for testing purposes."""

    def __init__(self, db_file="references_test.db"):
        _dirname = os.path.dirname(__file__)
        self._test_db_file = os.path.join(_dirname, "..", db_file)
        self._conn = sqlite3.connect(self._test_db_file)
        self._conn.row_factory = sqlite3.Row
        initialize_database(self._conn)

    def get_db_connection(self):
        return self._conn

    def cleanup(self):
        self._conn.close()
        os.remove(self._test_db_file)

    def save(self, ref):
        self._conn.execute("""
        INSERT OR REPLACE INTO "references"
            (reference_id, type, title, author, year, publisher)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        ref.ref_id,
        ref.ref_type,
        ref.title,
        ref.author,
        ref.year,
        ref.publisher
    ))
        self._conn.commit()
            
