import os
from pathlib import Path

from src.file_infos import FileInfo
from src.hasher import Hasher


class FileScan:
    @property
    def files(self):
        return self._files

    def __init__(self, directory: str, no_file_hash: bool):
        self._directory = directory
        self._files = []
        dir_path = Path(directory)

        hasher = Hasher()
        for path in dir_path.glob("**/*"):
            if path.is_dir():
                continue
            file_hash = None
            if not no_file_hash:
                file_hash = hasher.hash(path)
            self._files.append(
                FileInfo(
                    path=str(path.relative_to(dir_path)),
                    size_bytes=os.path.getsize(path.absolute()),
                    hash=file_hash,
                )
            )

    def __repr__(self):
        return f"FileScan('{self._directory}')"

    def __str__(self):
        return "\n".join([str(info) for info in self._files])

    def to_dict(self):
        return {"directory": self._directory, "files": [info.to_dict() for info in self._files]}
