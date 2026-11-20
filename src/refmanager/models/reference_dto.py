from dataclasses import dataclass


@dataclass
class ReferenceDto:
    """Data transfer object (DTO) for Reference"""

    ref_id: int
    ref_type: str
    title: str
    author: str
    year: int
    publisher: str
