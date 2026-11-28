import unittest
from dataclasses import replace

from refmanager.models.reference_dto import ReferenceDTO
from refmanager.services.reference_listing import (
    filter_references,
    list_references,
    sort_references,
)
from stub_io import StubIO


class FakeRepository:  # pylint: disable=too-few-public-methods
    """Korvaa oikean tietokannan testeissä."""

    def __init__(self, references):
        self._references = references

    def find_all(self):
        return list(self._references)


def make_ref(ref_id, author, year, title="Title"):
    return ReferenceDTO(
        ref_id=ref_id,
        ref_type="Kirja",
        title=title,
        author=author,
        year=year,
        publisher="",
        journal="",
        volume="",
        issue="",
        pages="",
        url="",
        accessed_on="",
        proceedings="",
        institution="",
        thesis_type="",
    )


class TestSortReferences(unittest.TestCase):
    def test_empty_list_stays_empty(self):
        self.assertEqual(sort_references([]), [])

    def test_sorted_by_author_ignoring_case(self):
        refs = [make_ref(1, "martin", 2008), make_ref(2, "Collins", 1991)]
        self.assertEqual([r.ref_id for r in sort_references(refs)], [2, 1])

    def test_same_author_sorted_by_year(self):
        refs = [make_ref(1, "Martin", 2010), make_ref(2, "Martin", 2008)]
        self.assertEqual([r.ref_id for r in sort_references(refs)], [2, 1])

    def test_same_author_and_year_sorted_by_title(self):
        refs = [make_ref(1, "Martin", 2008, "B"), make_ref(2, "Martin", 2008, "a")]
        self.assertEqual([r.ref_id for r in sort_references(refs)], [2, 1])


class TestListReferences(unittest.TestCase):
    def test_writes_one_line_per_reference_in_order(self):
        io = StubIO()
        repo = FakeRepository(
            [
                make_ref(1, "Martin", 2008, "Clean Code"),
                make_ref(2, "Collins", 1991, "Cognitive apprenticeship"),
            ]
        )
        list_references(repo, io)
        self.assertEqual(
            io.outputs,
            [
                "[Kirja]: Collins. Cognitive apprenticeship. 1991",
                "[Kirja]: Martin. Clean Code. 2008",
            ],
        )

    def test_uses_given_formatter(self):
        io = StubIO()
        list_references(
            FakeRepository([make_ref(1, "Martin", 2008)]),
            io,
            formatter=lambda ref: ref.author.upper(),
        )
        self.assertEqual(io.outputs, ["MARTIN"])

    def test_empty_repository_writes_no_references_message(self):
        io = StubIO()
        list_references(FakeRepository([]), io)
        self.assertEqual(
            io.outputs,
            ["Ei tallennettuja viitteitä. Lisää viite komennolla: refmanager new"],
        )


class TestFilterReferences(unittest.TestCase):
    def setUp(self):
        self.refs = [
            replace(
                make_ref(1, "Robert C. Martin", 2008, "Clean Code"),
                publisher="Prentice Hall",
            ),
            replace(
                make_ref(2, "Kent Beck", 1999, "Extreme Programming Explained"),
                publisher="Addison-Wesley",
            ),
            replace(
                make_ref(3, "Martin Fowler", 2018, "Refactoring"),
                publisher="Addison-Wesley",
            ),
            replace(
                make_ref(
                    4, "Kent Beck", 1999, "Embracing Change with Extreme Programming"
                ),
                ref_type="Artikkeli",
                journal="Computer",
                volume="32",
                issue="10",
            ),
            replace(
                make_ref(5, "Ken Schwaber", 1997, "SCRUM Development Process"),
                ref_type="Konferenssijulkaisu",
                proceedings="Business Object Design and Implementation",
            ),
            replace(
                make_ref(6, "Aino Virtanen", 2024, "Ketterät menetelmät opetuksessa"),
                ref_type="Opinnäytetyö tai väitöskirja",
                institution="Helsingin yliopisto",
                thesis_type="pro gradu",
            ),
        ]

    def _ids(self, references):
        return [ref.ref_id for ref in references]

    def test_no_filters_returns_all(self):
        result = filter_references(self.refs)
        self.assertEqual(self._ids(result), [1, 2, 3, 4, 5, 6])

    def test_empty_list_returns_empty(self):
        self.assertEqual(filter_references([], author="Martin"), [])

    def test_filter_by_author_partial_match(self):
        result = filter_references(self.refs, author="mart")
        self.assertEqual(self._ids(result), [1, 3])

    def test_filter_by_author_ignores_case(self):
        result = filter_references(self.refs, author="BECK")
        self.assertEqual(self._ids(result), [2, 4])

    def test_filter_by_year(self):
        result = filter_references(self.refs, year=1999)
        self.assertEqual(self._ids(result), [2, 4])

    def test_filter_by_publication_journal(self):
        result = filter_references(self.refs, publication="computer")
        self.assertEqual(self._ids(result), [4])

    def test_filter_by_publication_publisher(self):
        result = filter_references(self.refs, publication="Prentice")
        self.assertEqual(self._ids(result), [1])

    def test_filter_by_publication_proceedings(self):
        result = filter_references(self.refs, publication="business object")
        self.assertEqual(self._ids(result), [5])

    def test_filter_by_publication_institution(self):
        result = filter_references(self.refs, publication="helsingin")
        self.assertEqual(self._ids(result), [6])

    def test_combined_filters_must_all_match(self):
        result = filter_references(self.refs, author="martin", year=2018)
        self.assertEqual(self._ids(result), [3])

    def test_combined_author_and_publication(self):
        result = filter_references(self.refs, author="beck", publication="computer")
        self.assertEqual(self._ids(result), [4])

    def test_no_matches_returns_empty(self):
        result = filter_references(self.refs, author="Knuth")
        self.assertEqual(result, [])

    def test_does_not_modify_original_list(self):
        filter_references(self.refs, author="beck")
        self.assertEqual(len(self.refs), 6)
