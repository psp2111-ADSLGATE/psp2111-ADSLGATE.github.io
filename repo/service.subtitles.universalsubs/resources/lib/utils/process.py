# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, check_output
from typing import List

from resources.lib.utils.text import bytes_to_string


class Process:

    @staticmethod
    def build_exec_file_path(exec_name: str) -> Path:
        if os.name == 'nt' and not exec_name.endswith(".exe"):
            exec_name += ".exe"
        return exec_name

    @staticmethod
    def _process_creation_flags() -> int:
        return subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

    @staticmethod
    def run(args: List[str], throw_on_error: bool = False) -> CompletedProcess:
        return subprocess.run(args, check=throw_on_error, creationflags=Process._process_creation_flags())

    @staticmethod
    def capture_output(args: List[str], throw_on_error: bool = False) -> str:
        try:
            output_bytes = check_output(args, creationflags=Process._process_creation_flags())
            return bytes_to_string(output_bytes)
        except CalledProcessError as e:
            if throw_on_error:
                raise e
            return ""
