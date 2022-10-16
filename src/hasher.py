import hashlib
from pathlib import Path


class Hasher:
    def __init__(self, block_size: int = 65536):
        self._hasher = hashlib.md5()
        self._block_size = block_size

    def hash(self, file_path: Path):
        """
        Compute the md5 sum of a file
        """
        with file_path.open("rb") as text_io:
            buffer = text_io.read(self._block_size)
            while len(buffer) > 0:
                self._hasher.update(buffer)
                buffer = text_io.read(self._block_size)

        return self._hasher.hexdigest()
