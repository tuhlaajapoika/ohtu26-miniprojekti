"""Application configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Default database for the main program
DATABASE_FILE = PROJECT_ROOT / "data" / "references.db"
# Default database for tests
DATABASE_FILE_TESTS = PROJECT_ROOT / "data" / "references_test.db"
