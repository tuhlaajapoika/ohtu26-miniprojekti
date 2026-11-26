import unittest
import uuid

import refmanager.services.reference_to_dto as rtransform
from refmanager.models.reference import (
    Article,
    Book,
    Conference,
    Reference,
    Thesis,
    Website,
)
from refmanager.models.reference_dto import ReferenceDTO
from refmanager.models.reference_types import REFERENCE_TYPES


class TestReferenceToDTO(unittest.TestCase):
    def test_transform_reference_types_to_dto(self):
        cases = (
            (Reference, {}),
            (Article, {"volume": "10", "issue": "20", "pages": "300-350"}),
            (Book, {"publisher": "A Great Publisher"}),
            (Conference, {"proceedings": "Proc. USENIX Symp. Networked"}),
            (Thesis, {"institution": "JYU", "thesis_type": "pro gradu"}),
            (Website, {"url": "example.com", "accessed_on": "January 1, 1970"}),
        )

        for reference_class, special_fields in cases:
            with self.subTest(reference_class=reference_class.__name__):
                ref_id = uuid.uuid7()
                reference = reference_class(
                    "Title of the Work", "Author", 2026, **special_fields
                )
                ref_dto = rtransform.reference_to_dto(reference, ref_id)
                self.assertIsInstance(ref_dto, ReferenceDTO)
                self.assertEqual(ref_dto.ref_id, ref_id)
                self.assertEqual(ref_dto.ref_type, REFERENCE_TYPES.get(reference_class))
                self.assertEqual(ref_dto.title, reference.title)
                self.assertEqual(ref_dto.author, reference.author)
                self.assertEqual(ref_dto.year, reference.year)
                for name, value in special_fields.items():
                    self.assertEqual(getattr(ref_dto, name), value)
