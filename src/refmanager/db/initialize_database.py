@staticmethod
def drop_tables(connection):
    """Drop the "references" table from the database if it exists."""
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS "references";""")
    connection.commit()


@staticmethod
def create_tables(connection):
    """Create the "references" table in the database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "references" (
            reference_id INTEGER PRIMARY KEY,
            type TEXT,
            title TEXT,
            author TEXT,
            year INTEGER,
            publisher TEXT,
            journal TEXT,
            volume TEXT,
            issue TEXT,
            pages TEXT,
            url TEXT,
            accessed_on TEXT,
            proceedings TEXT,
            institution TEXT,
            thesis_type TEXT
        )
        """
    )
    connection.commit()


@staticmethod
def table_exists(connection) -> bool:
    """Check if the "references" table exists in the database.

    Args:
        connection: A SQLite database connection object.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor = connection.cursor()
    row = cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='references';
        """
    ).fetchone()
    return row is not None


@staticmethod
def initialize_database(connection):
    """Initialize the database with drop and create tables."""
    drop_tables(connection)
    create_tables(connection)
