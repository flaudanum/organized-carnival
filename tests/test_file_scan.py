import itertools

from src.file_scan import FileScan
from tests import TESTS_PATH


def test_recursive_file_scan_directory():
    test_dir_path = TESTS_PATH / "data" / "test_tree_dir"
    file_scan = FileScan(test_dir_path)
    ref_sizes_bytes = {
        "dir-a/dir-c/file5": 0,
        "dir-a/file3": 0,
        "dir-b/file4": 0,
        "file1": 1,
        "file2": 2,
    }

    # List of scanned file info items
    file_info_list = list(itertools.chain(*file_scan.files.values()))

    # Set of file paths
    file_info_paths = {info.path for info in file_info_list}

    # All file paths were reached
    assert file_info_paths == set(ref_sizes_bytes)

    # Check the completeness of the list of files
    assert {info.path for info in file_info_list} == set(ref_sizes_bytes)
    # Check the size of files
    for info in file_info_list:
        assert ref_sizes_bytes[info.path] == info.size_bytes
