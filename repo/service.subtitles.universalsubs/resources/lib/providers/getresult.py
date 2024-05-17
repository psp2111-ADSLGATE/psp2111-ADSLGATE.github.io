# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import chardet


class GetResult:

    _logger: logging.Logger = logging.getLogger('UniversalSubs.GetResult')

    def __init__(self):
        self.file_name: str = None
        self.content: bytes = None
        self.is_forced: bool = False
        self.is_hearing_impaired: bool = False
        self.provider_name: str = None

    def write_into(self, target_directory_path: Path, normalize_to_encoding="utf-8") -> Path:
        assert self.file_name is not None
        assert self.content is not None
        target_file_path = target_directory_path.joinpath(self.file_name)
        try:
            content = self.content
            if normalize_to_encoding:
                detected_encoding = chardet.detect(content)["encoding"]
                if detected_encoding:
                    content = content.decode(detected_encoding, "ignore").encode(normalize_to_encoding)
            with open(target_file_path, "wb") as file:
                file.write(content)
            return target_file_path
        except Exception as e:
            self._logger.fatal("Error writing into target path '%s'" % target_file_path, exc_info=True)
            raise e
