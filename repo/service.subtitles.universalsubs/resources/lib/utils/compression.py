# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from resources.lib.utils.process import Process


def _test_compression_type(file_path: Path = None, file_content: bytes = None) -> Literal['RAR', 'ZIP', '7Z']:
    if not file_content:
        assert file_path is not None
        with open(file_path, 'rb') as file:
            file_content: bytes = file.read()
    short_header: bytes = file_content[:4]
    if short_header == b"Rar!":
        return "RAR"
    elif short_header == b"PK\x03\x04":
        return "ZIP"
    elif file_content[:6] == b'7z\xbc\xaf\x27\x1c':
        return "7Z"
    else:
        return None


def _uncompress_with_7z(compressed_file_path: Path, target_dir_path: Path) -> bool:
    completed_process = Process.run([
        Compression.seven_zip_exec_path,
        "x",
        "-o" + str(target_dir_path),
        compressed_file_path])
    return not completed_process.returncode


try:
    import zipfile

    import xbmcvfs

    def _uncompress(compressed_file_path: Path, target_dir_path: Path, compression_type: Literal['RAR', 'ZIP', '7Z'] = None) -> bool:
        if not compression_type:
            compression_type = _test_compression_type(compressed_file_path)
        if compression_type == "ZIP":
            with zipfile.ZipFile(compressed_file_path, 'r') as zip_file:
                zip_file.extractall(target_dir_path)
            return True
        elif compression_type == "RAR":
            compressed_file_url = "archive" + "://" + quote_plus(compressed_file_path.as_posix()) + "/"
            directory_names, file_names = xbmcvfs.listdir(compressed_file_url)
            for file_name in file_names:
                if not file_name:  # dummy xbmcvfs implementation
                    return _uncompress_with_7z(compressed_file_path, target_dir_path)
                xbmcvfs.copy("%s%s" % (compressed_file_url, file_name), target_dir_path.joinpath(file_name).as_posix())
            return True
        return _uncompress_with_7z(compressed_file_path, target_dir_path)

except ImportError:
    import zipfile

    def _uncompress(compressed_file_path: Path, target_dir_path: Path, compression_type: Literal['RAR', 'ZIP', '7Z'] = None) -> bool:
        if not compression_type:
            compression_type = _test_compression_type(compressed_file_path)
        if compression_type == "ZIP":
            with zipfile.ZipFile(compressed_file_path, 'r') as zip_file:
                zip_file.extractall(target_dir_path)
            return True
        return _uncompress_with_7z(compressed_file_path, target_dir_path)


class Compression:

    # this will only work if 7-Zip is installed and available from the PATH
    seven_zip_exec_path: Path = "7z.exe" if os.name == 'nt' else "7z"

    @staticmethod
    def test_compression_type(file_path: Path = None, file_content: bytes = None) -> Literal['RAR', 'ZIP', '7Z']:
        return _test_compression_type(file_path, file_content)

    @staticmethod
    def uncompress(compressed_file_path: Path, target_dir_path: Path, compression_type: Literal['RAR', 'ZIP', '7Z'] = None) -> bool:
        return _uncompress(compressed_file_path, target_dir_path, compression_type)
