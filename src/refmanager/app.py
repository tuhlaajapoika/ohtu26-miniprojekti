import sys
from refmanager.models.reference_dto import ReferenceDto


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
            "5": "Opinnäytetyö tai väitöskirja"
        }

        while True:
            self.io.write(
                "Valitse lähdetyyppi:\n"
                "1 = Kirja\n"
                "2 = Artikkeli\n"
                "3 = Verkkosivu\n"
                "4 = Konferenssijulkaisu\n"
                "5 = Opinnäytetyö tai väitöskirja"
                )
            choice = self.io.read("Valinta: ")

            if choice in ref_options:
                return ref_options[choice]

            self.io.write("Virheellinen valinta. Valitse 1, 2, 3, 4 tai 5. ")

    def _collect_reference_details(self, ref_type):
        details = {
            "title": self.io.read("Nimi: "),
            "author": self.io.read("Tekijä(t): "),
            "year": int(self.io.read("Vuosi: ")),
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
        elif ref_type == "Artikkeli":
            details["volume"] = self.io.read(
                  "Vuosikerta (vol., voit jättää tyhjäksi):")
            details["issue"] = self.io.read(
                  "Numero (no., voit jättää tyhjäksi): ")
            details["pages"] = self.io.read("Sivut (voit jättää tyhjäksi): ")
        elif ref_type == "Verkkosivu":
            details["url"] = self.io.read("URL: ")
            details["accessed_on"] = self.io.read("Viittauspäivä (esim. 21.11.2026): ")
        elif ref_type == "Konferenssijulkaisu":
            details["proceedings"] = self.io.read("Julkaisun nimi tai julkaisusarja (voi jättää tyhjäksi): ")
        elif ref_type == "Opinnäytetyö tai väitöskirja":
            details["institution"] = self.io.read("Oppilaitos: ")
            details["thesis_type"] = self.io.read(
                 "Työn tyyppi (esimö AMK-opinnäytetyä, pro gradu, väitöskirja)")

        return details
