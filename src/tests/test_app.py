import unittest
from app_library import AppLibrary

class TestApp(unittest.TestCause):
    def test_new_reference(self):
        app = AppLibrary()
        app.input("Clean Code")
        app.input("Robert C. Martin")
        app.input("2008")
        app.input("Prentice hall")

        app.run_application("new")
        app.output_should_contain("Clean Code")