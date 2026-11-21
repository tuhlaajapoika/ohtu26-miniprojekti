import unittest

from app_library import AppLibrary


class TestApp(unittest.TestCase):
    def test_new_reference(self):
        app = AppLibrary()
        app.input("1")
        app.input("Clean Code")
        app.input("Robert C. Martin")
        app.input("2008")
        app.input("Prentice hall")

        app.run_application("new")
        self.assertTrue(app.outputs()[-1].startswith("Viite lisätty (ID: "))
