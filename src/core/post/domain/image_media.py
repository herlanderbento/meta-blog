from dataclasses import dataclass


@dataclass(frozen=True)
class ImageMedia:
    name: str
    raw_location: str
