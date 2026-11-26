"""Listing of saved references."""

from refmanager.services.reference_dto_formatter import format_reference_dto

NO_REFERENCES_MESSAGE = (
    "Ei tallennettuja viitteitä. Lisää viite komennolla: refmanager new"
)


def sort_references(references):
    """Return references sorted by author, year and title (case-insensitive)."""
    return sorted(
        references,
        key=lambda ref: (ref.author.lower(), ref.year, ref.title.lower()),
    )


def list_references(repository, io, formatter=format_reference_dto):
    """Write all references to io in sorted order, one per line.

    Writes a message instead if there are no references.
    """
    references = repository.find_all()
    if not references:
        io.write(NO_REFERENCES_MESSAGE)
        return
    for ref in sort_references(references):
        io.write(formatter(ref))
