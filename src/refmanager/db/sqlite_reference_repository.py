import os
import sqlite3

from refmanager.db.initialize_database import (
    create_tables,
    initialize_database,
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

        # TODO: remove init when create/delete program logic is implemented
        initialize_database(self.conn)

        if not table_exists(self.conn):
            raise RuntimeError("DB: 'references' table does not exist.")

    def get_db_connection(self):
        return self.conn

    def find_by_id(self, ref_id: int) -> ReferenceDto | None:
        cursor = self.conn.execute(
            """
            SELECT reference_id, type, title, author, year, publisher
                FROM "references"
                WHERE reference_id = ?;
            """,
            (ref_id,),
        )
        row = cursor.fetchone()
        if row is not None:
            # Change row to ReferenceDto object
            return ReferenceDto(
                ref_id=row[0],
                ref_type=row[1],
                title=row[2],
                author=row[3],
                year=row[4],
                publisher=row[5],
            )
        return None

    # TODO: or only INSERT with id set to NULL?
    def save(self, ref: ReferenceDto) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO
                "references" (reference_id, type, title, author, year, publisher)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
            (ref.ref_id, ref.ref_type, ref.title, ref.author, ref.year, ref.publisher),
        )
        self.conn.commit()
