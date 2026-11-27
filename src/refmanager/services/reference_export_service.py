from typing import TextIO

from refmanager.feature.export.reference_exporter import (
    BibtexReferenceExporter,
    ReferenceExporter,
)
from refmanager.models.reference import Article
from refmanager.models.reference_dto import ReferenceDTO


# WIP: export, not yet in use
class ReferenceExportService:  # pylint: disable=too-few-public-methods
    """Select references for export and delegate format serialization."""

    def __init__(self, repository, exporter: ReferenceExporter | None = None) -> None:
        self.repository = repository
        self.exporter = exporter or BibtexReferenceExporter()

    def export_by_type(self, ref_type: str, destination: TextIO) -> int:
        """Export references of one type and return the number exported."""
        if ref_type != Article.reference_type:
            raise NotImplementedError(
                f"Export is not implemented for reference type: {ref_type}"
            )

        references: list[ReferenceDTO] = [
            reference
            for reference in self.repository.find_all()
            if reference.ref_type == ref_type
        ]
        self.exporter.export(references, destination)
        return len(references)
