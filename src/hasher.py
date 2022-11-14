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
        with file_path.open("rb") as binary_io:
            byte_data = binary_io.read()
        return hashlib.md5(byte_data).hexdigest()
