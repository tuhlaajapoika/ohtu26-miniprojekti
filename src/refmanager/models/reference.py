from dataclasses import dataclass


@dataclass
class Reference:
    """
    Shared data for a reference.

    Includes mandatory fields for the DTO.
    """

    title: str
    author: str
    year: int


@dataclass
class Article(Reference):
    """An article reference."""

    volume: str = ""
    issue: str = ""
    pages: str = ""


@dataclass
class Book(Reference):
    """A book reference."""

    publisher: str = ""


@dataclass
class Conference(Reference):
    """A conference publication reference."""

    proceedings: str = ""


@dataclass
class Thesis(Reference):
    """A thesis reference."""

    institution: str = ""
    thesis_type: str = ""


@dataclass
class Website(Reference):
    """A website reference."""

    url: str = ""
    accessed_on: str = ""
