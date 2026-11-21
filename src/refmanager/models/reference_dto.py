from dataclasses import dataclass


@dataclass
class ReferenceDto:  # pylint: disable=too-many-instance-attributes
    """Data transfer object (DTO) for Reference"""

    ref_id: int | None
    ref_type: str
    title: str
    author: str
    year: int
    publisher: str
    journal: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    url: str = ""
    accessed_on: str = ""
    proceedings: str = ""
    institution: str = ""
    thesis_type: str = ""
