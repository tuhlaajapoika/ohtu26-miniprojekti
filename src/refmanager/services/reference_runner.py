import os
import uuid

from refmanager.exceptions import UserQuitException
from refmanager.models.reference_dto import ReferenceDTO
from refmanager.models.reference_types import REFERENCE_TYPES
from refmanager.services.reference_dto_formatter import format_reference_dto
from refmanager.services.reference_listing import list_references

# Reference type specific fields: (field name, prompt shown to the user)
EXTRA_FIELDS = {
    "Kirja": [
        ("publisher", "Kustantaja: "),
    ],
    "Artikkeli": [
        ("volume", "Vuosikerta (vol., voit jättää tyhjäksi):"),
        ("issue", "Numero (no., voit jättää tyhjäksi): "),
        ("pages", "Sivut (voit jättää tyhjäksi): "),
    ],
    "Verkkosivu": [
        ("url", "URL: "),
        ("accessed_on", "Viittauspäivä (esim. 21.11.2026): "),
    ],
    "Konferenssijulkaisu": [
        ("proceedings", "Julkaisun nimi tai julkaisusarja (voi jättää tyhjäksi): "),
    ],
    "Opinnäytetyö tai väitöskirja": [
        ("institution", "Oppilaitos: "),
        (
            "thesis_type",
            "Työn tyyppi (esim. AMK-opinnäytetyö, pro gradu, väitöskirja)",
        ),
    ],
}


class ReferenceRunner:
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io

    def run(self, command):
        match command:
            case "new":
                reference = self.create_reference()
                ref_id = self.repository.save(reference)
                self.io.write(f"Viite lisätty (ID: {ref_id})")
            case "list":
                list_references(
                    self.repository, self.io, formatter=format_reference_dto
                )
            case "export":
                self.io.write("Not implemented: export")
            case "quit":
                raise UserQuitException("Quitting the program.")

    def create_reference(self):
        ref_type = self._select_reference_type()
        details = self._collect_reference_details(ref_type)
        return ReferenceDTO(ref_id=uuid.uuid7(), ref_type=ref_type, **details)

    def _select_reference_type(self):
        # Iterate REFERENCE_TYPES
        _ref_options = {
            str(number): reference_type
            for number, reference_type in enumerate(REFERENCE_TYPES.values(), start=1)
        }

        while True:
            self.io.write("Valitse lähdetyyppi:")
            for option in _ref_options:
                self.io.write(f"[{option}] {_ref_options.get(option)}")
            self.io.write("[0] Lopeta")

            choice = self._ask(f"Valinta [0-{len(_ref_options.keys())}]: ")

            if choice == "0":
                raise UserQuitException("Quitting the program.")

            if choice in _ref_options:
                return _ref_options[choice]

            self.io.write(f"Virheellinen valinta.{os.linesep}")

    def _ask(self, prompt):
        """Read input from the user and quit if the user types 'quit'."""
        value = self.io.read(prompt)
        if value.strip().lower() == "quit":
            raise UserQuitException("Quitting the program.")
        return value

    def _collect_reference_details(self, ref_type):
        title = self._ask("Nimi: ")
        author = self._ask("Tekijä(t): ")
        year_input = self._ask("Vuosi: ")

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

        for field, prompt in EXTRA_FIELDS.get(ref_type, []):
            details[field] = self._ask(prompt)

        return details
