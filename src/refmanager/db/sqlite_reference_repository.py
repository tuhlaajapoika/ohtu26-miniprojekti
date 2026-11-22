import sqlite3
import uuid
from pathlib import Path

from refmanager.config import PROJECT_ROOT
from refmanager.db.initialize_database import create_tables, table_exists
from refmanager.db.schema import (
    FIND_ALL_REFERENCES_SQL,
    FIND_REFERENCES_BY_ID_SQL,
    INSERT_NEW_REFERENCE_SQL,
)
from refmanager.models.reference_dto import ReferenceDto
from refmanager.repositories.reference_repository import ReferenceRepository


class SqliteReferenceRepository(ReferenceRepository):
    """SQLite implementation of the reference data access interface."""

    def __init__(self, db_file):
        db_path = Path(db_file)
        if not db_path.is_absolute():
            db_path = PROJECT_ROOT / db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        create_tables(self.conn)

        # Remove init and use create (above) when proper program logic is implemented.
        # Clean database is needed until we have a stable program.
        # initialize_database(self.conn)

        if not table_exists(self.conn):
            raise sqlite3.OperationalError("'references' table does not exist.")

    def get_db_connection(self):
        return self.conn

    def close(self):
        """Close the database connection."""
        self.conn.commit()
        self.conn.close()

    def find_by_id(self, ref_id: uuid.UUID) -> ReferenceDto | None:
        cursor = self.conn.execute(FIND_REFERENCES_BY_ID_SQL, (str(ref_id),))
        row = cursor.fetchone()
        if row is not None:
            # Change row to ReferenceDto object
            return ReferenceDto(
                ref_id=uuid.UUID(row["reference_id"]),
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
                thesis_type=row["thesis_type"],
            )
        return None

    def save(self, ref: ReferenceDto) -> uuid.UUID:
        if ref.ref_id is None:
            ref.ref_id = uuid.uuid7()

        cursor = self.conn.execute(
            INSERT_NEW_REFERENCE_SQL,
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

        self.conn.commit()
        if cursor.rowcount != 1:
            raise RuntimeError(
                f"(database) Reference was not saved: {ref.ref_id}, {ref.title}"
            )
        return ref.ref_id

    def find_all(self) -> list[ReferenceDto]:
        cursor = self.conn.execute(FIND_ALL_REFERENCES_SQL)
        rows = cursor.fetchall()
        return [
            ReferenceDto(
                ref_id=uuid.UUID(row["reference_id"]),
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
                thesis_type=row["thesis_type"],
            )
            for row in rows
        ]
