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
                            ref_type = ref_options[choice]
                            break

                        self.io.write("Virheellinen valinta. Valitse 1, 2, 3, 4 tai 5. ")
                        
                    title = self.io.read("Otsikko: ")
                    author = self.io.read("Tekijä: ")
                    year = int(self.io.read("Vuosi: "))

                    if ref_type == "Kirja":
                        publisher = self.io.read("Kustantaja: ")
                    else:
                        publisher = ""
                            
                    reference = ReferenceDto(
                        ref_id=None,
                        ref_type=ref_type,
                        title=title,
                        author=author,
                        year=year,
                        publisher=publisher
                        )
                            
                    ref_id = self.repository.save(reference)
                    self.io.write(f"Viite lisätty (ID: {ref_id})")
                    self.io.write(f"{ref_type}: {title} - {author} ({year})")

                    if publisher:
                        self.io.write(f"Kustantaja: {publisher}")
                            
                case "list":
                    self.io.write("Not implemented: list")
                case "export":
                    self.io.write("Not implemented: export")
        except RuntimeError as e:
            self.io.write(f"{e}")
            sys.exit(1)
