# -*- coding: utf-8 -*-

import logging
import logging.config
import re
from pathlib import Path
from typing import Dict

from resources.lib.utils.json import from_json
from resources.lib.utils.yaml import from_yaml

ORIG_RECORD_FACTORY = logging.getLogRecordFactory()
ABBRV_NAMES: Dict[str, str] = {}


def _resolve_abbrv_name(name: str) -> str:
    abbrv_name = ABBRV_NAMES.get(name, None)
    if not abbrv_name:
        name_parts = name.split('.')
        abbrv_name_parts = []
        for index, name_part in enumerate(name_parts):
            if index < len(name_parts) - 1:
                abbrv_name_parts.append("".join(w[0] for w in re.findall(
                    r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name_part)))
            else:
                abbrv_name_parts.append(name_part)
        abbrv_name = ".".join(abbrv_name_parts)
    return abbrv_name


def _record_factory(*args, **kwargs) -> logging.LogRecord:
    record = ORIG_RECORD_FACTORY(*args, **kwargs)
    record.abbrv_name = _resolve_abbrv_name(record.name)
    return record


def init_logging_from_json(config_path: Path) -> None:
    with open(config_path, 'rt') as config_file:
        config = from_json(config_file.read())
        logging.config.dictConfig(config)
    logging.setLogRecordFactory(_record_factory)


def init_logging_from_yaml(config_path: Path) -> None:
    with open(config_path, 'rt') as config_file:
        config = from_yaml(config_file.read())
        logging.config.dictConfig(config)
    logging.setLogRecordFactory(_record_factory)


try:
    import xbmc
    from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGWARNING

    class KodiLogHandler(logging.Handler):

        def __init__(self) -> None:
            logging.Handler.__init__(self=self)

        def ___logging_level_to_kodi_level(self, levelno: int) -> int:
            if levelno == logging.DEBUG:
                # return LOGDEBUG
                return LOGINFO
            if levelno == logging.INFO:
                return LOGINFO
            if levelno == logging.WARNING:
                return LOGWARNING
            if levelno == logging.ERROR:
                return LOGERROR
            if levelno == logging.CRITICAL:
                return LOGFATAL
            return LOGFATAL

        def emit(self, record: logging.LogRecord) -> None:
            xbmc.log(self.formatter.format(record), self.___logging_level_to_kodi_level(record.levelno))

except ImportError:
    pass
