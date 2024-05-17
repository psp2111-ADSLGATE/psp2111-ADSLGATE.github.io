# -*- coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path, PosixPath, WindowsPath
from typing import Any

import yaml

from resources.lib.common.language import Language
from resources.lib.providers.getresult import GetResult


def language_representer(dumper: yaml.SafeDumper, value: Language) -> yaml.nodes.MappingNode:
    return dumper.represent_str(str(value))


def timedelta_representer(dumper: yaml.SafeDumper, value: timedelta) -> yaml.nodes.MappingNode:
    return dumper.represent_str(str(value))


def path_representer(dumper: yaml.SafeDumper, value: Path) -> yaml.nodes.MappingNode:
    return dumper.represent_str(str(value.resolve()))


def format_data_size(data_bytes: int) -> str:
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(data_bytes) < 1024.0:
            return f"{data_bytes:3.1f} {unit}B"
        data_bytes /= 1024.0
    return "{data_bytes:.1f} YB".format(data_bytes=data_bytes)


def get_result_representer(dumper: yaml.SafeDumper, value: GetResult) -> yaml.nodes.MappingNode:
    value_class = value.__class__
    return dumper.represent_mapping("!python/object:%s.%s" % (value_class.__module__, value_class.__name__), {
        "provider_name": value.provider_name,
        "file_name": value.file_name,
        "is_forced": value.is_forced,
        "is_hearing_impaired": value.is_hearing_impaired,
        "content_size":  format_data_size(len(value.content)) if value.content else None,
    })


yaml.representer.Representer.add_representer(Language, language_representer)
yaml.representer.Representer.add_representer(Path, path_representer)
yaml.representer.Representer.add_representer(WindowsPath, path_representer)
yaml.representer.Representer.add_representer(PosixPath, path_representer)
yaml.representer.Representer.add_representer(timedelta, timedelta_representer)
yaml.representer.Representer.add_representer(GetResult, get_result_representer)


def to_yaml(data: Any) -> str:
    return yaml.dump(data, width=120)


def from_yaml(text: str):
    return yaml.safe_load(text)
