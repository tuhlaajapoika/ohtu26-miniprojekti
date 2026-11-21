import unittest
from unittest.mock import patch

from refmanager.io.console_io import ConsoleIO


class TestConsoleIO(unittest.TestCase):
    def test_write(self):
        _io = ConsoleIO()
        with patch("builtins.print") as print_mock:
            _io.write(value="this_test")

        print_mock.assert_called_once_with("this_test")

    def test_read(self):
        _io = ConsoleIO()
        with patch("builtins.input", return_value="this_test") as input_mock:
            result = _io.read(prompt="Test prompt: ")

        input_mock.assert_called_once_with("Test prompt: ")
        self.assertEqual(result, "this_test")
