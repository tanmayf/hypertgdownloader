import os
import pytest
from pathlib import Path
from hypertgdownloader.utils import ensure_directory_exists, get_temp_part_path

def test_ensure_directory_exists(tmp_path):
    directory = tmp_path / "test_dir"
    ensure_directory_exists(str(directory))
    assert directory.exists()

def test_get_temp_part_path():
    directory = "downloads"
    filename = "video.mp4"
    idx = 1
    expected = os.path.join(directory, "video.mp4.part01")
    assert get_temp_part_path(directory, filename, idx) == expected
