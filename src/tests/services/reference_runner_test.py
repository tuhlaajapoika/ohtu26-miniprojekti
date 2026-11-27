import unittest
import uuid

from refmanager.exceptions import UserQuitException
from refmanager.models.reference_dto import ReferenceDTO
from refmanager.services.reference_runner import ReferenceRunner


class FakeRepository:
    """Korvaa oikean tietokannan testeissä."""

    def __init__(self, references):
        self.references = list(references)
        self.delete_ids = []

    def find_all(self):
        return list(self.references)

    def delete(self, ref_id):
        self.delete_ids.append(ref_id)
        self.references = [
            reference for reference in self.references if reference.ref_id != ref_id
        ]


class FakeIO:
    """Korvaa käyttäjän syötteet ja ohjelman tulosteet testeissä."""

    def __init__(self, inputs):
        self.inputs = list(inputs)
        self.outputs = []

    def read(self, prompt):
        del prompt
        return self.inputs.pop(0)

    def write(self, text):
        self.outputs.append(text)

# pylint: disable=duplicate-code
def make_ref(ref_id, title="Test reference"):
    return ReferenceDTO(
        ref_id=ref_id,
        ref_type="Kirja",
        title=title,
        author="Test author",
        year=2026,
        publisher="Test bublisher",
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


class TestDeleteReference(unittest.TestCase):
    def test_deletes_selected_reference_when_confirmed(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["1", "k"])
        runner = ReferenceRunner(repository, io)

        runner.delete_reference()

        self.assertEqual(repository.delete_ids, [reference.ref_id])
        self.assertEqual(repository.references, [])
        self.assertIn("Viite poistettu.", io.outputs)

    def test_does_not_delete_reference_when_cancelled(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["1", "e"])
        runner = ReferenceRunner(repository, io)

        runner.delete_reference()

        self.assertEqual(repository.delete_ids, [])
        self.assertEqual(repository.references, [reference])
        self.assertIn("Poistaminen peruutettu.", io.outputs)

    def test_empty_repository_does_not_ask_for_selection(self):
        repository = FakeRepository([])
        io = FakeIO([])
        runner = ReferenceRunner(repository, io)

        runner.delete_reference()

        self.assertEqual(repository.delete_ids, [])
        self.assertIn("Ei viitteitä lisätty.", io.outputs)

    def test_delete_command_calls_delete_reference(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["1", "k"])
        runner = ReferenceRunner(repository, io)

        runner.run("delete")

        self.assertEqual(repository.delete_ids, [reference.ref_id])

    def test_invalid_selection_then_valid_selection(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["x", "1", "k"])
        runner = ReferenceRunner(repository, io)

        runner.delete_reference()

        self.assertEqual(repository.delete_ids, [reference.ref_id])
        self.assertTrue(any("Virheellinen valinta." in output for output in io.outputs))

    def test_quit_when_selecting_reference_to_delete(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["0"])
        runner = ReferenceRunner(repository, io)

        with self.assertRaises(UserQuitException):
            runner.delete_reference()

    def test_incalid_confirmation_does_not_delete_reference(self):
        reference = make_ref(uuid.uuid7())
        repository = FakeRepository([reference])
        io = FakeIO(["1", "x"])
        runner = ReferenceRunner(repository, io)

        runner.delete_reference()

        self.assertEqual(repository.delete_ids, [])
        self.assertIn("Virheellinen valinta.", io.outputs)
