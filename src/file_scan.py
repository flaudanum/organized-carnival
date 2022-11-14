import os
import sys
from collections import defaultdict
from pathlib import Path

import orjson

from src import SCAN_DUMP_FILENAME
from src.file_infos import FileInfo
from src.hasher import Hasher


class FileScan:
    @property
    def files(self):
        return self._files

    @property
    def hashes(self):
        return set(self._files)

    def __init__(self, directory: str, no_file_hash: bool = False):
        self._directory = directory
        self._files = defaultdict(list)

        # Creates a dummy object
        if directory == "":
            return

        dir_path = Path(directory)

        hasher = Hasher()
        for path in dir_path.glob("**/*"):
            # TODO: recursive scan
            if path.is_dir():
                continue
            # Skips scan dump files
            if path.name == SCAN_DUMP_FILENAME:
                continue
            path_str = str(path.relative_to(dir_path))
            size_bytes = os.path.getsize(path.absolute())
            file_hash = None

            if no_file_hash:
                hash_int = hash(path_str + str(size_bytes))
                key = "-" + hex(hash_int)[3:] if hash_int < 0 else hex(hash_int)[2:]
            else:
                file_hash = hasher.hash(path)
                key = file_hash[:8]

            self._files[key].append(FileInfo(path=path_str, size_bytes=size_bytes, hash=file_hash))

    def __repr__(self):
        return f"FileScan('{self._directory}')"

    def __str__(self):
        return "\n".join([str(info) for info in self._files.values()])

    def dump(self, directory):
        file_scan_dict = {
            "directory": self._directory,
            "files": {key: [info.to_dict() for info in infos] for key, infos in self._files.items()},
        }
        scan_dump_path = Path(directory) / SCAN_DUMP_FILENAME
        dump_exists = scan_dump_path.is_file()
        with scan_dump_path.open("wb") as binary_io:
            binary_io.write(orjson.dumps(file_scan_dict))
        print(f"{'Overwritten' if dump_exists else 'Saved'} scan dump at '{scan_dump_path.absolute()}'")

    @staticmethod
    def from_dump(directory: str):
        dump_file_path = Path(directory) / SCAN_DUMP_FILENAME
        if not dump_file_path.is_file():
            sys.stderr.write(f"Dump file {directory} does not exist\n")
            sys.stderr.write(f"Starts scanning directory {directory} with file hash computation.\n")
            sys.stderr.flush()
            return FileScan(directory=directory)

        with dump_file_path.open("rb") as binary_io:
            file_scan_dict = orjson.loads(binary_io.read())

        file_scan = FileScan(directory="")
        file_scan._directory = file_scan_dict["directory"]
        file_scan_dict_files: dict[str, list[FileInfo]] = {
            key: [FileInfo.from_dict(info) for info in infos_dict]
            for key, infos_dict in file_scan_dict["files"].items()
        }
        file_scan._files.update(file_scan_dict_files)

        return file_scan
