from enum import Enum as EnumPython

import orjson
from flask.json.provider import JSONProvider
from sqlalchemy_serializer import SerializerMixin


class SemesterEnum(EnumPython):
    SPRING = "Spring"
    FALL = "Fall"
    SUMMER = "Summer"


class LocationEnum(EnumPython):
    TBD = "TBD"
    AMOS_EATON = "Amos Eaton"
    CARNEGIE = "Carnegie"
    CBIS = "Center for Biotechnology and Interdisciplinary Studies"
    CCI = "Center for Computational Innovations"
    CII = "Low Center for Industrial Innovation (CII)"
    COGSWELL = "Cogswell Laboratory"
    DCC = "Darrin Communications Center"
    EMPAC = "Experimental Media and Performing Arts Center"
    GREENE = "Greene Library"
    JEC = "Jonsson Engineering Center"
    JROWL = "Jonsson-Rowland Science Center"
    LALLY = "Lally Hall"
    LINAC = "LINAC Facility (Gaerttner Laboratory)"
    MRC = "Materials Research Center"
    PITTSBURGH = "Pittsburgh Building"
    RICKETTS = "Ricketts Building"
    SAGE = "Russell Sage Laboratory"
    VCC = "Voorhees Computing Center"
    WALKER = "Walker Laboratory"
    WEST = "West Hall"
    WINSLOW = "Winslow Building"
    REMOTE = "Remote"


class OrJSONProvider(JSONProvider):
    def dumps(self, obj, *, option=None, **kwargs):
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC

        return orjson.dumps(obj, option=option).decode()

    def loads(self, s, **kwargs):
        return orjson.loads(s)


class CustomSerializerMixin(SerializerMixin):
    # date_format = "%s"  # Unixtimestamp (seconds)
    # datetime_format = "%Y %b %d %H:%M:%S.%f"
    # time_format = "%H:%M.%f"
    decimal_format = "{:0>10.3}"
