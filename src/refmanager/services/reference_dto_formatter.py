"""Formatting of references for the listing."""

from dataclasses import fields

from refmanager.models.reference import Reference
from refmanager.models.reference_dto import ReferenceDTO
from refmanager.models.reference_types import REFERENCE_TYPES
from refmanager.services.reference_formatters import (
    DEFAULT_REFERENCE_FORMATTER,
    ReferenceFormatter,
)


def format_reference_dto(
    ref: ReferenceDTO,
    formatter: ReferenceFormatter = DEFAULT_REFERENCE_FORMATTER,
) -> str:
    """Format a reference DTO using the given citation-style strategy."""
    # Iterate REFERENCE_TYPES and choose reference class.
    reference_class = next(
        (
            reference_class
            for reference_class, ref_type in REFERENCE_TYPES.items()
            if ref_type == ref.ref_type
        ),
        None,
    )
    if reference_class is None:
        # Default to the base type.
        reference = Reference(ref.title, ref.author, ref.year)
    else:
        details = {
            field.name: getattr(ref, field.name)
            for field in fields(reference_class)
            # details excluding base class information.
            if field.name not in {"title", "author", "year"}
        }
        reference = reference_class(ref.title, ref.author, ref.year, **details)
    return formatter.format(reference, type_label=ref.ref_type)
