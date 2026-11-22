import os
import shutil
import tempfile
import unittest

from app_library import AppLibrary
from refmanager.config import DATABASE_FILE_TESTS


class TestApp(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._temp_dir)
        self._db_file = os.path.join(self._temp_dir, DATABASE_FILE_TESTS)

    def test_new_reference(self):
        app = AppLibrary(self._db_file)
        app.input("1")
        app.input("Clean Code")
        app.input("Robert C. Martin")
        app.input("2008")
        app.input("Prentice hall")

        app.run_application("new")
        self.assertTrue(app.outputs()[-1].startswith("Viite lisätty (ID: "))
