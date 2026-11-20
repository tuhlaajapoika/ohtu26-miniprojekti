from dataclasses import dataclass


@dataclass
class ReferenceDto:
    """Data transfer object (DTO) for Reference"""

    id: int
    type: str
    title: str
    author: str
    year: int
    publisher: str
