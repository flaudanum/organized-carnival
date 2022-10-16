import os
from pathlib import Path

from src.file_infos import FileInfo
from src.hasher import Hasher


class FileScan:
    @property
    def files(self):
        return self._files

    def __init__(self, directory: str):
        self._directory = directory
        self._files = []
        dir_path = Path(directory)

        hasher = Hasher()
        for path in dir_path.glob("**/*"):
            if path.is_dir():
                continue
            self._files.append(
                FileInfo(
                    path=str(path.relative_to(dir_path)),
                    size_bytes=os.path.getsize(path.absolute()),
                    hash=hasher.hash(path),
                )
            )

    def __repr__(self):
        return f"FileScan('{self._directory}')"

    def __str__(self):
        return "\n".join([str(info) for info in self._files])
