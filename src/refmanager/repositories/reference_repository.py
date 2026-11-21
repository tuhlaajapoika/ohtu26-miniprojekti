from abc import ABC, abstractmethod

from refmanager.models.reference_dto import ReferenceDto


class ReferenceRepository(ABC):
    """DAO interface for managing references in the database."""

    @abstractmethod
    def find_by_id(self, ref_id: int) -> ReferenceDto | None:
        """Find a reference by id

        Args:
            ref_id (int): id of the reference

        Returns:
            ReferenceDto | None: Reference DTO if found, else None
        """

    @abstractmethod
    def save(self, ref: ReferenceDto) -> int:
        """Save reference and return its database ID."""
