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


def _matches_publication(ref, publication):
    """Return True if publication is found in any publication field."""
    fields = (ref.journal, ref.proceedings, ref.publisher, ref.institution)
    search = publication.lower()
    return any(search in (field or "").lower() for field in fields)


def filter_references(references, author=None, year=None, publication=None):
    """Return references matching all given filters.
    Author and publication are case-insensitive partial matches, year is an
    exact match.
    """
    result = []
    for ref in references:
        if author is not None and author.lower() not in ref.author.lower():
            continue
        if year is not None and ref.year != year:
            continue
        if publication is not None and not _matches_publication(ref, publication):
            continue
        result.append(ref)
    return result
