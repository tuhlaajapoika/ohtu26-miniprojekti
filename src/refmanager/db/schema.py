# Create references table to the database
CREATE_REFERENCES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS "references" (
    reference_id TEXT PRIMARY KEY,
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
);
"""

# Get all references from the database
FIND_ALL_REFERENCES_SQL = """
SELECT
    reference_id,
    type,
    title,
    author,
    year,
    publisher,
    journal,
    volume,
    issue,
    pages,
    url,
    accessed_on,
    proceedings,
    institution,
    thesis_type
FROM "references";
"""

# Find by ID
FIND_REFERENCES_BY_ID_SQL = """
SELECT
    reference_id,
    type,
    title,
    author,
    year,
    publisher,
    journal,
    volume,
    issue,
    pages,
    url,
    accessed_on,
    proceedings,
    institution,
    thesis_type
FROM "references" WHERE reference_id = ?;
"""

# Save new reference to the database.
# Using named style instead of qmark style.
# See: https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries # pylint: disable=line-too-long
INSERT_NEW_REFERENCE_SQL = """
INSERT OR REPLACE INTO "references" (
    reference_id,
    type,
    title,
    author,
    year,
    publisher,
    journal,
    volume,
    issue,
    pages,
    url,
    accessed_on,
    proceedings,
    institution,
    thesis_type)
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
