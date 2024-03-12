from enum import Enum as EnumPython

import orjson
from flask.json.provider import JSONProvider


class SemesterEnum(EnumPython):
    SPRING = "Spring"
    FALL = "Fall"
    SUMMER = "Summer"


class OrJSONProvider(JSONProvider):
    def dumps(self, obj, *, option=None, **kwargs):
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC

        return orjson.dumps(obj, option=option).decode()

    def loads(self, s, **kwargs):
        return orjson.loads(s)
