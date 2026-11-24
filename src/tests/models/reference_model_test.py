import unittest

from refmanager.models.reference import (
    Article,
    Book,
    Conference,
    Reference,
    Thesis,
    Website,
)


class TestReferenceModels(unittest.TestCase):
    def test_subclasses_share_base_fields_and_default_special_fields(self):
        cases = (
            (Article, {"volume": "", "issue": "", "pages": ""}),
            (Book, {"publisher": ""}),
            (Conference, {"proceedings": ""}),
            (Thesis, {"institution": "", "thesis_type": ""}),
            (Website, {"url": "", "accessed_on": ""}),
        )

        for reference_class, special_fields in cases:
            with self.subTest(reference_class=reference_class.__name__):
                reference = reference_class("Title", "Author", 2024)

                self.assertIsInstance(reference, Reference)
                self.assertEqual(reference.title, "Title")
                self.assertEqual(reference.author, "Author")
                self.assertEqual(reference.year, 2024)
                for name, value in special_fields.items():
                    self.assertEqual(getattr(reference, name), value)
