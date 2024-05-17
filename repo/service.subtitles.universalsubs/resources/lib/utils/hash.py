# -*- coding: utf-8 -*-

import os
import struct
from io import BufferedReader
from pathlib import Path
from typing import Tuple

__longlong_format_char = 'q'
__byte_size = struct.calcsize(__longlong_format_char)


def _add_64bit_chksum(file: BufferedReader, base_file_hash: int) -> int:
    range_value = 65536 / __byte_size
    range_value = round(range_value)
    for _ in range(range_value):
        try:
            chunk = file.read(__byte_size)
        except:
            chunk = file.read(__byte_size)
        (value,) = struct.unpack(__longlong_format_char, chunk)
        base_file_hash += value
        base_file_hash &= 0xFFFFFFFFFFFFFFFF
    return base_file_hash

# https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
# filehash = filesize + 64bit sum of the first and last 64k of the file


def compute_size_and_hash(file_path: Path) -> Tuple[int, str]:
    with open(file_path, 'rb') as file:
        filesize = os.path.getsize(file_path)
        if filesize < 65536 * 2:
            return filesize, None
        filehash = _add_64bit_chksum(file, filesize)
        file.seek(filesize - 65536, os.SEEK_SET)
        filehash = _add_64bit_chksum(file, filehash)
        return filesize, "%016x" % filehash
