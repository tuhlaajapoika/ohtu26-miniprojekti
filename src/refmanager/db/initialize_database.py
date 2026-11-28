from sqlite3 import Connection

from refmanager.db.schema import CREATE_REFERENCES_TABLE_SQL


@staticmethod
def drop_tables(connection: Connection):
    """Drop the "references" table from the database if it exists."""
    cursor = connection.cursor()
    try:
        cursor.execute("""DROP TABLE IF EXISTS "references";""")
    finally:
        cursor.close()
        connection.commit()


@staticmethod
def create_tables(connection: Connection):
    """Create the "references" table in the database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_REFERENCES_TABLE_SQL)
    finally:
        cursor.close()
        connection.commit()


@staticmethod
def table_exists(connection: Connection) -> bool:
    """Check if the "references" table exists in the database.

    Args:
        connection: A SQLite database connection object.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor = connection.cursor()
    try:
        row = cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='references';
            """
        ).fetchone()
        return row is not None
    finally:
        cursor.close()


@staticmethod
def initialize_database(connection: Connection):
    """Initialize the database with drop and create tables."""
    drop_tables(connection)
    create_tables(connection)
