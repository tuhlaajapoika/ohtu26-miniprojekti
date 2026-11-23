"""Formatting of references for the listing."""

from refmanager.models.reference_dto import ReferenceDTO


def _book_details(ref: ReferenceDTO) -> list[str]:
    parts = []
    if ref.publisher:
        parts.append(ref.publisher)
    return parts


def _article_details(ref: ReferenceDTO) -> list[str]:
    parts = []
    if ref.volume:
        parts.append(f"vol. {ref.volume}")
    if ref.issue:
        parts.append(f"no. {ref.issue}")
    if ref.pages:
        parts.append(f"s. {ref.pages}")
    return parts


def _website_details(ref: ReferenceDTO) -> list[str]:
    parts = []
    if ref.url:
        parts.append(ref.url)
    if ref.accessed_on:
        parts.append(f"luettu {ref.accessed_on}")
    return parts


def _conference_details(ref: ReferenceDTO) -> list[str]:
    parts = []
    if ref.proceedings:
        parts.append(ref.proceedings)
    return parts


def _thesis_details(ref: ReferenceDTO) -> list[str]:
    parts = []
    if ref.institution:
        parts.append(ref.institution)
    if ref.thesis_type:
        parts.append(ref.thesis_type)
    return parts


_DETAILS_BY_TYPE = {
    "Kirja": _book_details,
    "Artikkeli": _article_details,
    "Verkkosivu": _website_details,
    "Konferenssijulkaisu": _conference_details,
    "Opinnäytetyö tai väitöskirja": _thesis_details,
}


def format_reference(ref: ReferenceDTO) -> str:
    """Return a readable one-line presentation of a reference."""
    text = f"{ref.ref_type}: {ref.author} ({ref.year}). {ref.title}."

    details_function = _DETAILS_BY_TYPE.get(ref.ref_type)
    parts = details_function(ref) if details_function else []

    if parts:
        text += " " + ", ".join(parts) + "."
    return text
