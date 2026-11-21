import sys
from refmanager.models.reference_dto import ReferenceDto
from refmanager.services.reference_listing import list_references


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
                        
                    title = self.io.read("Nimi: ")
                    author = self.io.read("Tekijä(t): ")
                    year = int(self.io.read("Vuosi: "))

                    publisher = ""
                    journal = ""
                    volume = ""
                    issue = ""
                    pages = ""
                    url = ""
                    accessed_on = ""
                    proceedings = ""
                    institution = ""
                    thesis_type = ""

                    if ref_type == "Kirja":
                        publisher = self.io.read("Kustantaja: ")
                    elif ref_type == "Artikkeli":
                        volume = self.io.read("Vuosikerta (vol., voit jättää tyhjäksi): ")
                        issue = self.io.read("Numero (no., voit jättää tyhjäksi): ")
                        pages = self.io.read("Sivut (voit jättää tyhjäksi): ")
                    elif ref_type == "Verkkosivu":
                        url = self.io.read("URL: ")
                        accessed_on = self.io.read("Viittauspäivä (esim. 21.11.2026): ")
                    elif ref_type == "Konferenssijulkaisu":
                        proceedings = self.io.read("Julkaisun nimi tai julkaisusarja (voi jättää tyhjäksi): ")
                    elif ref_type == "Opinnäytetyö tai väitöskirja":
                        institution = self.io.read("Oppilaitos: ")
                        thesis_type = self.io.read("Työn tyyppi (esimö AMK-opinnäytetyä, pro gradu, väitöskirja)")
                        
                            
                    reference = ReferenceDto(
                        ref_id=None,
                        ref_type=ref_type,
                        title=title,
                        author=author,
                        year=year,
                        publisher=publisher,
                        journal=journal,
                        volume=volume,
                        issue=issue,
                        pages=pages,
                        url=url,
                        accessed_on=accessed_on,
                        proceedings=proceedings,
                        institution=institution,
                        thesis_type=thesis_type
                        )
                            
                    ref_id = self.repository.save(reference)
                    self.io.write(f"Viite lisätty (ID: {ref_id})")

                    # TODO: Viitteen muotoilu lisätään tähän
                   


                    
                            
                case "list":
                    list_references(self.repository, self.io)
                case "export":
                    self.io.write("Not implemented: export")
        except RuntimeError as e:
            self.io.write(f"{e}")
            sys.exit(1)
