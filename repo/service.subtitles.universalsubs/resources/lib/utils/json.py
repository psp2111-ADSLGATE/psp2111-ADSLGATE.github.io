# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from json import JSONDecoder, JSONEncoder
from pathlib import Path


class CustomObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return obj.as_posix()
        if isinstance(obj, timedelta):
            return obj.total_seconds()
        try:
            return obj.__dict__
        except:
            return {}


class JSONWithCommentsDecoder(JSONDecoder):
    def __init__(self, **kw):
        super().__init__(**kw)

    def decode(self, s: str):
        s = '\n'.join(l if not l.lstrip().startswith('//') else '' for l in s.split('\n'))
        return super().decode(s)


def to_json(obj) -> str:
    return json.dumps(obj, cls=CustomObjectEncoder)


def from_json(json_text: str):
    return json.loads(json_text, cls=JSONWithCommentsDecoder)
