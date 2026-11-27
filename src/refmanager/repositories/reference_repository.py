import uuid
from abc import ABC, abstractmethod

from refmanager.models.reference_dto import ReferenceDTO


class ReferenceRepository(ABC):
    """DAO interface for managing references in the database."""

    @abstractmethod
    def find_by_id(self, ref_id: uuid.UUID) -> ReferenceDTO | None:
        """Find a reference by id

        Args:
            ref_id (uuid.UUID): id of the reference

        Returns:
            ReferenceDTO | None: Reference DTO if found, else None
        """

    @abstractmethod
    def save(self, ref: ReferenceDTO) -> uuid.UUID:
        """Save reference and return its UUID."""

    @abstractmethod
    def find_all(self) -> list[ReferenceDTO]:
        """Return all references. Empty list if none"""

    @abstractmethod
    def delete(self, ref_id: uuid.UUID) -> None:
        """Delete a reference by id."""
