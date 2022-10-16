from src.hasher import Hasher
from tests import TESTS_PATH


def test_hash():
    hasher = Hasher()
    file_path = TESTS_PATH / "data" / "binary-file.png"
    file_hash = hasher.hash(file_path)

    # Note: provided by Linux md5sum
    expected_md5sum = "341df9679d229d39e7d334af978d2ec7"
    assert expected_md5sum == file_hash
