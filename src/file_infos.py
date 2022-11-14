from dataclasses import dataclass


@dataclass
class FileInfo:
    path: str
    size_bytes: int
    hash: str | None

    def to_dict(self):
        return {"path": self.path, "size_bytes": self.size_bytes, "hash": self.hash}

    @staticmethod
    def from_dict(info_dict: dict):
        return FileInfo(**info_dict)
