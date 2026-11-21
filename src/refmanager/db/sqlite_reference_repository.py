import os
import sqlite3

from refmanager.db.initialize_database import (
    create_tables,
    table_exists,
)
from refmanager.models.reference_dto import ReferenceDto
from refmanager.repositories.reference_repository import ReferenceRepository


class SqliteReferenceRepository(ReferenceRepository):
    """SQLite implementation of the reference data access interface."""

    def __init__(self, db_file):
        dirname = os.path.dirname(__file__)
        db_full_path = os.path.join(dirname, "..", "..", "..", db_file)
        self.conn = sqlite3.connect(db_full_path)
        self.conn.row_factory = sqlite3.Row
        create_tables(self.conn)

        # remove init when create/delete program logic is implemented
        #initialize_database(self.conn)

        if not table_exists(self.conn):
            raise RuntimeError("DB: 'references' table does not exist.")

    def get_db_connection(self):
        return self.conn

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def find_by_id(self, ref_id: int) -> ReferenceDto | None:
        cursor = self.conn.execute(
            """
            SELECT reference_id, type, title, author, year,
            publisher, journal, volume, issue, pages, url, accessed_on,
            proceedings, institution, thesis_type
                FROM "references"
                WHERE reference_id = ?;
            """,
            (ref_id,),
        )
        row = cursor.fetchone()
        if row is not None:
            # Change row to ReferenceDto object
            return ReferenceDto(
                ref_id=row["reference_id"],
                ref_type=row["type"],
                title=row["title"],
                author=row["author"],
                year=row["year"],
                publisher=row["publisher"],
                journal=row["journal"],
                volume=row["volume"],
                issue=row["issue"],
                pages=row["pages"],
                url=row["url"],
                accessed_on=row["accessed_on"],
                proceedings=row["proceedings"],
                institution=row["institution"],
                thesis_type=row["thesis_type"]
            )
        return None

    def save(self, ref: ReferenceDto) -> int:
        cursor = self.conn.execute(
            """
            INSERT OR REPLACE INTO "references" (
            reference_id, type, title, author, year, publisher,
            journal, volume, issue, pages, url, accessed_on, proceedings,
            institution, thesis_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
    (
        ref.ref_id,
        ref.ref_type,
        ref.title,
        ref.author,
        ref.year,
        ref.publisher,
        ref.journal,
        ref.volume,
        ref.issue,
        ref.pages,
        ref.url,
        ref.accessed_on,
        ref.proceedings,
        ref.institution,
        ref.thesis_type,
        ),
    )

        self.conn.commit()
        return cursor.lastrowid
