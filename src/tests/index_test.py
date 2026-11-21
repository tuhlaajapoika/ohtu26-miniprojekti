import os
import sys
import unittest
from unittest.mock import Mock, patch

from refmanager import index


class TestIndex(unittest.TestCase):
    def test_main_initializes_services_and_runs_selected_command(self):
        for command in ("new", "list", "export"):
            with self.subTest(command=command):
                console_io = Mock()
                repository = Mock()
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
                app.run.assert_called_once_with(command=command)

    def test_main_requires_a_command(self):
        with (
            patch.object(sys, "argv", ["refmanager"]),
            self.assertRaises(SystemExit) as context,
        ):
            index.main()

        self.assertEqual(context.exception.code, 2)  # exit status 2

    def test_main_rejects_unknown_command(self):
        with (
            patch.object(sys, "argv", ["refmanager", "unknown"]),
            self.assertRaises(SystemExit) as context,
        ):
            index.main()

        self.assertEqual(context.exception.code, 2)  # exit status 2

    def test_main_closes_database_and_exits_on_keyboard_interrupt(self):
        console_io = Mock()
        connection = Mock()
        repository = Mock()
        repository.get_db_connection.return_value = connection
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
            patch("refmanager.index.print") as print_mock,
            patch("refmanager.index.sys.exit") as exit_mock,
        ):
            index.main()

        print_mock.assert_called_once_with(
            f"{os.linesep}User interrupt captured.", console_io
        )
        repository.get_db_connection.assert_called_once_with()
        connection.close.assert_called_once_with()
        exit_mock.assert_called_once_with(130)
