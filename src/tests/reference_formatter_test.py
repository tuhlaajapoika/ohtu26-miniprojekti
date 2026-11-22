import unittest
import uuid

from refmanager.models.reference_dto import ReferenceDto
from refmanager.services.reference_formatter import format_reference


def make_reference(ref_type, **fields):
    defaults = {
        "ref_id": uuid.uuid7(),
        "ref_type": ref_type,
        "title": "Title",
        "author": "Author",
        "year": 2026,
        "publisher": "",
    }
    defaults.update(fields)
    return ReferenceDto(**defaults)


class TestFormatReference(unittest.TestCase):
    """Tests for formatting a single reference for the listing."""

    def test_book_shows_publisher(self):
        reference = make_reference(
            "Kirja",
            title="Clean Code",
            author="Robert C. Martin",
            year=2008,
            publisher="Prentice Hall",
        )
        self.assertEqual(
            format_reference(reference),
            "Kirja: Robert C. Martin (2008). Clean Code. Prentice Hall.",
        )

    def test_article_shows_volume_issue_and_pages(self):
        reference = make_reference(
            "Artikkeli",
            title="Cognitive apprenticeship",
            author="Allan Collins",
            year=1991,
            volume="6",
            issue="11",
            pages="38-46",
        )
        self.assertEqual(
            format_reference(reference),
            "Artikkeli: Allan Collins (1991). Cognitive apprenticeship. "
            "vol. 6, no. 11, s. 38-46.",
        )

    def test_article_without_optional_fields_has_no_empty_labels(self):
        reference = make_reference("Artikkeli", title="Short paper", year=2020)
        formatted = format_reference(reference)
        self.assertEqual(formatted, "Artikkeli: Author (2020). Short paper.")
        self.assertNotIn("vol.", formatted)
        self.assertNotIn("no.", formatted)

    def test_website_shows_url_and_access_date(self):
        reference = make_reference(
            "Verkkosivu",
            title="Python documentation",
            author="Python Software Foundation",
            url="https://docs.python.org",
            accessed_on="21.11.2026",
        )
        self.assertEqual(
            format_reference(reference),
            "Verkkosivu: Python Software Foundation (2026). Python documentation. "
            "https://docs.python.org, luettu 21.11.2026.",
        )

    def test_conference_paper_shows_proceedings(self):
        reference = make_reference(
            "Konferenssijulkaisu",
            title="Agile in practice",
            author="Matti Meikäläinen",
            year=2024,
            proceedings="Proceedings of XP 2024",
        )
        self.assertEqual(
            format_reference(reference),
            "Konferenssijulkaisu: Matti Meikäläinen (2024). Agile in practice. "
            "Proceedings of XP 2024.",
        )

    def test_thesis_shows_institution_and_thesis_type(self):
        reference = make_reference(
            "Opinnäytetyö tai väitöskirja",
            title="Viitteiden hallinta",
            author="Maija Virtanen",
            year=2025,
            institution="Jyväskylän yliopisto",
            thesis_type="pro gradu",
        )
        self.assertEqual(
            format_reference(reference),
            "Opinnäytetyö tai väitöskirja: Maija Virtanen (2025). Viitteiden hallinta. "
            "Jyväskylän yliopisto, pro gradu.",
        )

    def test_unknown_type_shows_only_common_fields(self):
        reference = make_reference("Muu", publisher="Ignored Publisher")
        self.assertEqual(format_reference(reference), "Muu: Author (2026). Title.")

    def test_reference_id_is_not_shown(self):
        reference = make_reference("Kirja", publisher="Prentice Hall")
        self.assertNotIn(str(reference.ref_id), format_reference(reference))
