import uuid
from dataclasses import asdict

from refmanager.models.reference import Reference
from refmanager.models.reference_dto import ReferenceDTO
from refmanager.models.reference_types import REFERENCE_TYPES


def reference_to_dto(reference: Reference, ref_id: uuid.UUID) -> ReferenceDTO:
    """Transforms a reference type into a `ReferenceDTO` object

    Args:
        reference (Reference): reference to be transformed
        ref_id (uuid.UUID): generated id for the reference

    Returns:
        ReferenceDTO: a DTO object of the reference
    """
    details = asdict(reference)
    return ReferenceDTO(
        ref_id=ref_id,
        ref_type=REFERENCE_TYPES[type(reference)],
        **details,
    )
