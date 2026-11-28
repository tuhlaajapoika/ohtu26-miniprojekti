import sqlite3
import uuid
from pathlib import Path

from refmanager.config import PROJECT_ROOT
from refmanager.db.initialize_database import create_tables, table_exists
from refmanager.db.schema import (
    DELETE_REFERENCE_SQL,
    FIND_ALL_REFERENCES_SQL,
    FIND_REFERENCES_BY_ID_SQL,
    INSERT_OR_REPLACE_REFERENCE_SQL,
)
from refmanager.models.reference_dto import ReferenceDTO
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
            raise sqlite3.IntegrityError(
                "(database) 'references' table does not exist."
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_db_connection(self):
        return self.conn

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def find_by_id(self, ref_id: uuid.UUID) -> ReferenceDTO | None:
        cursor = self.conn.cursor()
        try:
            cursor.execute(FIND_REFERENCES_BY_ID_SQL, (str(ref_id),))
            row = cursor.fetchone()
            if row is not None:
                return ReferenceDTO(
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
        finally:
            cursor.close()

    def save(self, ref: ReferenceDTO) -> uuid.UUID:
        # Connection as context manager
        with self.conn as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    INSERT_OR_REPLACE_REFERENCE_SQL,
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
                # Only checks if INSERT was succesful.
                if cursor.rowcount != 1:
                    raise RuntimeError(
                        f"(database) Reference was not saved: {ref.ref_id}, {ref.title}"
                    )
                return ref.ref_id
            finally:
                cursor.close()

    def find_all(self) -> list[ReferenceDTO]:
        cursor = self.conn.cursor()
        try:
            cursor.execute(FIND_ALL_REFERENCES_SQL)
            rows = cursor.fetchall()
            return [
                ReferenceDTO(
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
        finally:
            cursor.close()

    def delete(self, ref_id: uuid.UUID) -> None:
        # Connection as context manager
        with self.conn as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    DELETE_REFERENCE_SQL,
                    (str(ref_id),),
                )
                if cursor.rowcount != 1:
                    raise RuntimeError(
                        f"(database) Reference was not deleted: {ref_id}"
                    )
            finally:
                cursor.close()
