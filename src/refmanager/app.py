import sys
from textwrap import dedent

from refmanager.models.reference_dto import ReferenceDto


class UserQuitException(Exception):
    """An exception raised when the user chooses to quit the application."""


class App:
    """A class that represents the main application for managing references."""

    def __init__(self, ref_repository, io):
        self.repository = ref_repository
        self.io = io

    def run(self, command):
        try:
            match command:
                case "new":
                    reference = self.create_reference()
                    ref_id = self.repository.save(reference)
                    self.io.write(f"Viite lisätty (ID: {ref_id})")
                case "list":
                    self.io.write("Not implemented: list")
                case "export":
                    self.io.write("Not implemented: export")
                case "quit":
                    raise UserQuitException()
        except UserQuitException:
            self.io.write("Quitting the program.")
            sys.exit(0)
        except RuntimeError as e:
            self.io.write(f"{e}")
            sys.exit(1)

    def create_reference(self):
        ref_type = self._select_reference_type()
        details = self._collect_reference_details(ref_type)
        return ReferenceDto(ref_id=None, ref_type=ref_type, **details)

    def _select_reference_type(self):
        ref_options = {
            "1": "Kirja",
            "2": "Artikkeli",
            "3": "Verkkosivu",
            "4": "Konferenssijulkaisu",
            "5": "Opinnäytetyö tai väitöskirja",
        }

        while True:
            # detent: prevent indentation
            self.io.write(
                dedent(
                    """\
                Valitse lähdetyyppi:
                1 = Kirja
                2 = Artikkeli
                3 = Verkkosivu
                4 = Konferenssijulkaisu
                5 = Opinnäytetyö tai väitöskirja
                """
                )
            )
            choice = self.io.read("Valinta: ")

            if choice.strip().lower() == "quit":
                raise UserQuitException()

            if choice in ref_options:
                return ref_options[choice]

            self.io.write("Virheellinen valinta. Valitse 1, 2, 3, 4 tai 5. ")

    def _collect_reference_details(self, ref_type):
        title = self.io.read("Nimi: ")
        if title.strip().lower() == "quit":
            raise UserQuitException()

        author = self.io.read("Tekijä(t): ")
        if author.strip().lower() == "quit":
            raise UserQuitException()

        year_input = self.io.read("Vuosi: ")
        if year_input.strip().lower() == "quit":
            raise UserQuitException()

        details = {
            "title": title,
            "author": author,
            "year": int(year_input),
            "publisher": "",
            "journal": "",
            "volume": "",
            "issue": "",
            "pages": "",
            "url": "",
            "accessed_on": "",
            "proceedings": "",
            "institution": "",
            "thesis_type": "",
        }
        if ref_type == "Kirja":
            details["publisher"] = self.io.read("Kustantaja: ")
            if details["publisher"].strip().lower() == "quit":
                raise UserQuitException()
        elif ref_type == "Artikkeli":
            details["volume"] = self.io.read("Vuosikerta (vol., voit jättää tyhjäksi):")
            if details["volume"].strip().lower() == "quit":
                raise UserQuitException()
            details["issue"] = self.io.read("Numero (no., voit jättää tyhjäksi): ")
            if details["issue"].strip().lower() == "quit":
                raise UserQuitException()
            details["pages"] = self.io.read("Sivut (voit jättää tyhjäksi): ")
            if details["pages"].strip().lower() == "quit":
                raise UserQuitException()
        elif ref_type == "Verkkosivu":
            details["url"] = self.io.read("URL: ")
            if details["url"].strip().lower() == "quit":
                raise UserQuitException()
            details["accessed_on"] = self.io.read("Viittauspäivä (esim. 21.11.2026): ")
            if details["accessed_on"].strip().lower() == "quit":
                raise UserQuitException()
        elif ref_type == "Konferenssijulkaisu":
            details["proceedings"] = self.io.read(
                "Julkaisun nimi tai julkaisusarja (voi jättää tyhjäksi): "
            )
            if details["proceedings"].strip().lower() == "quit":
                raise UserQuitException()
        elif ref_type == "Opinnäytetyö tai väitöskirja":
            details["institution"] = self.io.read("Oppilaitos: ")
            if details["institution"].strip().lower() == "quit":
                raise UserQuitException()
            details["thesis_type"] = self.io.read(
                "Työn tyyppi (esim. AMK-opinnäytetyö, pro gradu, väitöskirja)"
            )
            if details["thesis_type"].strip().lower() == "quit":
                raise UserQuitException()

        return details
