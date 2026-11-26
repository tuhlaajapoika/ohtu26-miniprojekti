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
            _STUB_INSERT_OR_REPLACE_REFERENCE_SQL,
            {
                "reference_id": str(ref.ref_id),
                "type": ref.ref_type,
                "title": ref.title,
                "author": ref.author,
                "year": ref.year,
                "publisher": ref.publisher,
                "journal": ref.journal,
                "volume": ref.volume,
                "issue": ref.issue,
                "pages": ref.pages,
                "url": ref.url,
                "accessed_on": ref.accessed_on,
                "proceedings": ref.proceedings,
                "institution": ref.institution,
                "thesis_type": ref.thesis_type,
            },
        )
        self._conn.commit()


_STUB_REFERENCE_COLUMNS = (
    "reference_id",
    "type",
    "title",
    "author",
    "year",
    "publisher",
    "journal",
    "volume",
    "issue",
    "pages",
    "url",
    "accessed_on",
    "proceedings",
    "institution",
    "thesis_type",
)
_STUB_REFERENCE_COLUMN_LIST = ",\n    ".join(_STUB_REFERENCE_COLUMNS)

_STUB_INSERT_OR_REPLACE_REFERENCE_SQL = f"""
    INSERT OR REPLACE INTO "references" (
        {_STUB_REFERENCE_COLUMN_LIST}
    )
    VALUES (
        :reference_id,
        :type,
        :title,
        :author,
        :year,
        :publisher,
        :journal,
        :volume,
        :issue,
        :pages,
        :url,
        :accessed_on,
        :proceedings,
        :institution,
        :thesis_type
    );
"""
