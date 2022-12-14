import itertools
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import orjson

from src import SCAN_DUMP_FILENAME
from src.file_infos import FileInfo
from src.hasher import Hasher

DATETIME_FORMAT = "%y%m%d-%H:%M:%S%z"


class FileScan:
    @property
    def created_at(self):
        return self._created_at

    @property
    def files(self):
        return self._files

    @property
    def hashes(self):
        return set(self._files)

    def __init__(self, directory: str, no_file_hash: bool = False, complete_rescan: bool = False):
        self._directory = directory
        self._files: defaultdict[str, list[FileInfo]] = defaultdict(list)
        local_tz = datetime.now().astimezone().tzinfo
        self._created_at = datetime.now(tz=local_tz)
        self._updated_at = datetime.now(tz=local_tz)

        # Creates a dummy object
        if directory == "":
            return

        dir_path = Path(directory)
        relative_file_paths = set()

        if not complete_rescan and (Path(directory) / SCAN_DUMP_FILENAME).is_file():
            saved_scan = FileScan.from_dump(directory)
            self._files = saved_scan.files
            self._created_at = saved_scan.created_at
            relative_file_paths = {
                str(Path(info.path)) for info in itertools.chain(*self._files.values())
            }
        elif not (Path(directory) / SCAN_DUMP_FILENAME).is_file():
            complete_rescan = True

        hasher = Hasher()
        for path in dir_path.glob("**/*"):
            if path.is_dir():
                continue
            # Skips scan dump files
            if path.name == SCAN_DUMP_FILENAME:
                continue

            path_str = str(path.relative_to(dir_path))

            # File path already scanned
            if not complete_rescan and path_str in relative_file_paths:
                continue

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
            "created_at": self._created_at.strftime(DATETIME_FORMAT),
            "updated_at": self._updated_at.strftime(DATETIME_FORMAT),
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

        file_scan._created_at = datetime.strptime(file_scan_dict["created_at"], DATETIME_FORMAT)
        file_scan._updated_at = datetime.strptime(file_scan_dict["updated_at"], DATETIME_FORMAT)

        return file_scan
