import unittest
import uuid

from refmanager.models.reference_dto import ReferenceDTO
from refmanager.services.reference_dto_formatter import format_reference_dto


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
    return ReferenceDTO(**defaults)


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
            format_reference_dto(reference),
            "[Kirja]: Robert C. Martin. Clean Code. Prentice Hall, 2008",
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
            format_reference_dto(reference),
            "[Artikkeli]: Allan Collins. Cognitive apprenticeship. "
            "vol. 6, no. 11, s. 38-46, 1991",
        )

    def test_article_without_optional_fields_has_no_empty_labels(self):
        reference = make_reference("Artikkeli", title="Short paper", year=2020)
        formatted = format_reference_dto(reference)
        self.assertEqual(formatted, "[Artikkeli]: Author. Short paper. 2020")
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
            format_reference_dto(reference),
            "[Verkkosivu]: Python Software Foundation. Python documentation. "
            "https://docs.python.org, luettu 21.11.2026, 2026",
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
            format_reference_dto(reference),
            "[Konferenssijulkaisu]: Matti Meikäläinen. Agile in practice. "
            "Proceedings of XP 2024, 2024",
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
            format_reference_dto(reference),
            "[Opinnäytetyö tai väitöskirja]: Maija Virtanen. Viitteiden hallinta. "
            "Jyväskylän yliopisto, pro gradu, 2025",
        )

    def test_unknown_type_shows_only_common_fields(self):
        reference = make_reference("Muu", publisher="Ignored Publisher")
        self.assertEqual(format_reference_dto(reference), "[Muu]: Author. Title. 2026")

    def test_reference_id_is_not_shown(self):
        reference = make_reference("Kirja", publisher="Prentice Hall")
        self.assertNotIn(str(reference.ref_id), format_reference_dto(reference))

    def test_uses_a_custom_formatter_strategy(self):
        class CustomFormatter:  # pylint: disable=too-few-public-methods
            def format(self, reference, type_label=None):
                return f"{type_label}:{reference.title}"

        reference = make_reference("Kirja", title="Clean Code")

        self.assertEqual(
            format_reference_dto(reference, formatter=CustomFormatter()),
            "Kirja:Clean Code",
        )
