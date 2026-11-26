import unittest

from refmanager.models.reference_dto import ReferenceDTO
from refmanager.services.reference_listing import list_references, sort_references
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
