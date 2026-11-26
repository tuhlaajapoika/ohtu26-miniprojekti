from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Reference:
    """
    Shared data for a reference.

    Includes mandatory fields for the DTO.
    """

    title: str
    author: str
    year: int

    reference_type: ClassVar[str] = "Muu"


@dataclass
class Article(Reference):
    """An article reference."""

    reference_type: ClassVar[str] = "Artikkeli"

    volume: str = ""
    issue: str = ""
    pages: str = ""


@dataclass
class Book(Reference):
    """A book reference."""

    reference_type: ClassVar[str] = "Kirja"

    publisher: str = ""


@dataclass
class Conference(Reference):
    """A conference publication reference."""

    reference_type: ClassVar[str] = "Konferenssijulkaisu"

    proceedings: str = ""


@dataclass
class Thesis(Reference):
    """A thesis reference."""

    reference_type: ClassVar[str] = "Opinnäytetyö tai väitöskirja"

    institution: str = ""
    thesis_type: str = ""


@dataclass
class Website(Reference):
    """A website reference."""

    reference_type: ClassVar[str] = "Verkkosivu"

    url: str = ""
    accessed_on: str = ""
