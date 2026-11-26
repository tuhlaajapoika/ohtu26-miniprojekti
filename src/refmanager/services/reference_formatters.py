"""Formatting strategies for reference models."""
# Define formatters in this file if different citation styles are needed.

from typing import Protocol

from refmanager.models.reference import (
    Article,
    Book,
    Conference,
    Reference,
    Thesis,
    Website,
)


class ReferenceFormatter(Protocol):  # pylint: disable=too-few-public-methods
    """Interface implemented by citation-style formatters."""

    def format(self, reference: Reference, type_label: str | None = None) -> str:
        """Return the reference rendered in a particular style."""


class ListingReferenceFormatter:  # pylint: disable=too-few-public-methods
    """Format references for the current human-readable listing."""

    def format(self, reference: Reference, type_label: str | None = None) -> str:
        """Render a reference; optionally override its displayed type label."""

        _label = reference.reference_type if type_label is None else type_label
        text = f"[{_label}]: {reference.author}. {reference.title}."
        details = self._details(reference)
        # append details
        if details:
            text += " " + ", ".join(details) + ","
        return f"{text} {reference.year}"

    @staticmethod
    def _details(reference: Reference) -> tuple[str, ...]:
        """Return non-empty display details for the reference subtype."""

        if isinstance(reference, Article):
            return tuple(
                detail
                for value, detail in (
                    (reference.volume, f"vol. {reference.volume}"),
                    (reference.issue, f"no. {reference.issue}"),
                    (reference.pages, f"s. {reference.pages}"),
                )
                if value
            )
        if isinstance(reference, Book):
            return (reference.publisher,) if reference.publisher else ()
        if isinstance(reference, Conference):
            return (reference.proceedings,) if reference.proceedings else ()
        if isinstance(reference, Thesis):
            return tuple(
                value
                for value in (reference.institution, reference.thesis_type)
                if value
            )
        if isinstance(reference, Website):
            details = []
            if reference.url:
                details.append(reference.url)
            if reference.accessed_on:
                details.append(f"luettu {reference.accessed_on}")
            return tuple(details)
        return ()


DEFAULT_REFERENCE_FORMATTER = ListingReferenceFormatter()
