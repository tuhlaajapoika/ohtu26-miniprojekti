import uuid
from collections.abc import Iterable
from typing import Protocol, TextIO

from bibtexparser import entrypoint
from bibtexparser.library import Library
from bibtexparser.model import Block, Entry, Field

from refmanager.models.reference import Article
from refmanager.models.reference_dto import ReferenceDTO


# WIP: export, not yet in use
class ReferenceExporter(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for serializing references to an output format."""

    def export(self, references: Iterable[ReferenceDTO], destination: TextIO) -> None:
        """Serialize references into the provided text destination."""


# WIP: export, not yet in use
class BibtexReferenceExporter:
    """Serialize article references as BibTeX entries."""

    def export(self, references: Iterable[ReferenceDTO], destination: TextIO) -> None:
        blocks: list[Block] = [self.to_entry(reference) for reference in references]
        entrypoint.write_file(destination, Library(blocks=blocks))

    @staticmethod
    def to_entry(reference: ReferenceDTO) -> Entry:
        """Convert one article DTO into a BibTeX entry."""
        if reference.ref_type != Article.reference_type:
            raise ValueError(
                f"BibTeX article export does not support type: {reference.ref_type}"
            )

        fields = [
            Field("author", reference.author),
            Field("title", reference.title),
            Field("year", str(reference.year)),
        ]
        optional_fields = (
            ("journal", reference.journal),
            ("volume", reference.volume),
            ("number", reference.issue),
            ("pages", reference.pages),
        )
        fields.extend(
            Field(field_name, value) for field_name, value in optional_fields if value
        )
        return Entry(
            entry_type="article",
            key=BibtexReferenceExporter._entry_key(reference.ref_id),
            fields=fields,
        )

    @staticmethod
    def _entry_key(ref_id: uuid.UUID | None) -> str:
        """Create a unique provisional key from the persisted reference id."""
        if ref_id is None:
            raise ValueError("Cannot export a reference without a saved reference id")
        return f"ref_{ref_id.hex}"
