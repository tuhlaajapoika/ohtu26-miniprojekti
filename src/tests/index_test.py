import argparse
import os
import sqlite3
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import MagicMock, Mock, patch

from refmanager import index
from refmanager.exceptions import UserQuitException


class TestIndex(unittest.TestCase):
    def test_main_initializes_services_and_runs_selected_command(self):
        for command in ("new", "list", "export"):
            with self.subTest(command=command):
                console_io = Mock()
                repository = MagicMock()
                repository.__enter__.return_value = repository
                app = Mock()

                with (
                    patch.object(sys, "argv", ["refmanager", command]),
                    patch("refmanager.index.ConsoleIO", return_value=console_io),
                    patch(
                        "refmanager.index.SqliteReferenceRepository",
                        return_value=repository,
                    ) as repository_class,
                    patch("refmanager.index.App", return_value=app) as app_class,
                ):
                    index.main()

                repository_class.assert_called_once_with(db_file=index.DATABASE_FILE)
                app_class.assert_called_once_with(
                    ref_repository=repository,
                    io=console_io,
                )
                if command == "export":
                    app.run.assert_called_once_with(
                        command=command,
                        export_path="references.bib",
                    )
                else:
                    app.run.assert_called_once_with(command=command)

    def test_tags_argument_is_a_list(self):
        command = "new"
        tags = ("tag.1", "tag.2", "tag.3", "many-tags")
        expected = argparse.Namespace(command=command, tag=list(tags))
        parsed_args = []
        original_parse_args = argparse.ArgumentParser.parse_args

        def capture_parse_args(parser, args=None, namespace=None):
            result = original_parse_args(parser, args, namespace)
            parsed_args.append(result)
            return result

        console_io = Mock()
        repository = MagicMock()
        repository.__enter__.return_value = repository
        app = Mock()

        with (
            patch.object(sys, "argv", ["refmanager", command, "--tag", *tags]),
            patch.object(argparse.ArgumentParser, "parse_args", capture_parse_args),
            patch("refmanager.index.ConsoleIO", return_value=console_io),
            patch(
                "refmanager.index.SqliteReferenceRepository",
                return_value=repository,
            ),
            patch("refmanager.index.App", return_value=app),
        ):
            index.main()

        self.assertEqual(parsed_args[0], expected)
        self.assertIsInstance(parsed_args[0].tag, list)

    def test_main_displays_available_commands_when_no_command_is_passed(self):
        help_usage_positional_args = (
            "positional arguments:",
            "COMMAND",
            "new       Create a new reference",
            "list      List all references",
            "export    Export references to BibTex format",
            "quit      Quit the program",
        )
        output = StringIO()
        with patch.object(sys, "argv", ["refmanager"]), redirect_stdout(output):
            index.main()

        for line in help_usage_positional_args:
            self.assertIn(line, output.getvalue())

    def test_main_rejects_unknown_command(self):
        with (
            patch.object(sys, "argv", ["refmanager", "unknown"]),
            self.assertRaises(SystemExit) as context,
        ):
            index.main()

        self.assertEqual(context.exception.code, 2)  # exit status 2

    def test_main_closes_database_and_exits_on_keyboard_interrupt(self):
        console_io = Mock()
        repository = MagicMock()
        repository.__enter__.return_value = repository
        app = Mock()
        app.run.side_effect = KeyboardInterrupt

        with (
            patch.object(sys, "argv", ["refmanager", "list"]),
            patch("refmanager.index.ConsoleIO", return_value=console_io),
            patch(
                "refmanager.index.SqliteReferenceRepository",
                return_value=repository,
            ),
            patch("refmanager.index.App", return_value=app),
            patch("refmanager.index.sys.exit") as exit_mock,
        ):
            index.main()

        console_io.write.assert_called_once_with(
            f"{os.linesep}User interrupt captured."
        )
        repository.__exit__.assert_called_once()
        exit_mock.assert_called_once_with(130)

    def test_main_closes_database_and_exits_on_user_quit(self):
        console_io = Mock()
        repository = MagicMock()
        repository.__enter__.return_value = repository
        app = Mock()
        app.run.side_effect = UserQuitException("Quitting the program.")

        with (
            patch.object(sys, "argv", ["refmanager", "quit"]),
            patch("refmanager.index.ConsoleIO", return_value=console_io),
            patch(
                "refmanager.index.SqliteReferenceRepository",
                return_value=repository,
            ),
            patch("refmanager.index.App", return_value=app),
            patch("refmanager.index.sys.exit") as exit_mock,
        ):
            index.main()
        console_io.write.assert_called_once_with("Quitting the program.")
        repository.__exit__.assert_called_once()
        exit_mock.assert_called_once_with(0)

    def test_main_runtime_error(self):
        console_io = Mock()
        repository = MagicMock()
        repository.__enter__.return_value = repository
        app = Mock()
        app.run.side_effect = RuntimeError("test RuntimeError")

        with (
            patch.object(sys, "argv", ["refmanager", "list"]),
            patch("refmanager.index.ConsoleIO", return_value=console_io),
            patch(
                "refmanager.index.SqliteReferenceRepository",
                return_value=repository,
            ),
            patch("refmanager.index.App", return_value=app),
            patch("refmanager.index.sys.exit") as exit_mock,
        ):
            index.main()

        console_io.write.assert_called_once_with("ERROR: test RuntimeError")
        exit_mock.assert_called_once_with(1)

    def test_main_sqlite_error(self):
        console_io = Mock()
        repository = MagicMock()
        repository.__enter__.return_value = repository
        app = Mock()
        app.run.side_effect = sqlite3.IntegrityError("test IntegrityError")

        with (
            patch.object(sys, "argv", ["refmanager", "list"]),
            patch("refmanager.index.ConsoleIO", return_value=console_io),
            patch(
                "refmanager.index.SqliteReferenceRepository",
                return_value=repository,
            ),
            patch("refmanager.index.App", return_value=app),
            patch("refmanager.index.sys.exit") as exit_mock,
        ):
            index.main()

        console_io.write.assert_called_once_with("ERROR: test IntegrityError")
        exit_mock.assert_called_once_with(1)
