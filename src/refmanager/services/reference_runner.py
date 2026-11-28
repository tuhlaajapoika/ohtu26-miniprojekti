import os
import uuid
from pathlib import Path

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

def normalize_tags(raw: str | list[str]) -> str:
    """Turn '--tag a b' or ' a, b ,, ' into 'a,b'."""
    items = [raw] if isinstance(raw, str) else raw
    tags = [part.strip() for item in items for part in item.split(",")]
    return ",".join(tag for tag in tags if tag)


class ReferenceRunner:
    def __init__(self, repository, io):
        self.repository = repository
        self.io = io
        # WIP: export, not yet in use
        # self.export_service = ReferenceExportService(
        #    repository, BibtexReferenceExporter()
        # )

    def run(self, command, export_path: str | Path = "references.bib", tags=None):
        match command:
            case "new":
                reference = self.create_reference(tags)
                ref_id = self.repository.save(reference)
                self.io.write(f"Viite lisätty (ID: {ref_id})")
            case "delete":
                self.delete_reference()
            case "list":
                list_references(
                    self.repository, self.io, formatter=format_reference_dto
                )
            case "export":
                self.export_references(export_path)
            case "quit":
                raise UserQuitException("Quitting the program.")

    def create_reference(self, tags=None):
        ref_type = self._select_reference_type()
        details = self._collect_reference_details(ref_type, tags)
        return ReferenceDTO(ref_id=uuid.uuid7(), ref_type=ref_type, **details)

    def delete_reference(self):
        reference = self._select_reference_to_delete()

        if reference is None:
            return

        self._when_deleting_reference(reference)

    def export_references(self, export_path: str | Path = "references.bib"):
        """Export article references to a BibTeX file."""
        # WIP: export, not yet in use
        # path = Path(export_path)
        # with path.open("w", encoding="utf-8") as destination:
        #    count = self.export_service.export_by_type(
        #        Article.reference_type, destination
        #    )
        # self.io.write(f"Artikkeliviitteet viety tiedostoon {path} ({count} kpl).")
        self.io.write(f"Not implemented: export -o {export_path}")

    def _select_reference_to_delete(self):

        references = self.repository.find_all()

        if not references:
            self.io.write("Ei viitteitä lisätty.")
            return None

        _ref_options = {
            str(number): reference
            for number, reference in enumerate(references, start=1)
        }

        while True:
            self.io.write("Valitse poistettava viite:")
            self.io.write("[0] Lopeta")
            for option, reference in _ref_options.items():
                self.io.write(f"[{option}] {format_reference_dto(reference)}")

            choice = self._ask(f"Valinta [0-{len(_ref_options)}]: ")

            if choice == "0":
                raise UserQuitException("Quitting the program.")

            if choice in _ref_options:
                return _ref_options[choice]

            self.io.write(f"Virheellinen valinta.{os.linesep}")

    def _when_deleting_reference(self, reference):
        self.io.write(
            "Oletko varma, että haluat poistaa tämän viitteen? Muutokset ovat pysyviä."
        )
        self.io.write(format_reference_dto(reference))

        choice = self._ask("Poistetaanko viite [k/e]: ")

        if choice.lower() == "k":
            self.repository.delete(reference.ref_id)
            self.io.write("Viite poistettu.")
        elif choice.lower() == "e":
            self.io.write("Poistaminen peruutettu.")
        else:
            self.io.write("Virheellinen valinta.")

    def _select_reference_type(self):
        # Iterate REFERENCE_TYPES
        _ref_options = {
            str(number): reference_type
            for number, reference_type in enumerate(REFERENCE_TYPES.values(), start=1)
        }

        while True:
            self.io.write("Valitse lähdetyyppi:")
            self.io.write("[0] Lopeta")
            for option in _ref_options:
                self.io.write(f"[{option}] {_ref_options.get(option)}")

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

    def _collect_reference_details(self, ref_type, tags=None):
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

        # Ask for tags in the form only if --tag was not given.
        if tags is None:
            tags = self._ask("Tagit (erota pilkulla, voit jättää tyhjäksi): ")
        details["tags"] = normalize_tags(tags)

        return details
