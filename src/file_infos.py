from dataclasses import dataclass


@dataclass
class FileInfo:
    path: str
    size_bytes: int
    hash: str
