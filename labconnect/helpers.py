from enum import Enum as EnumPython

import orjson
from flask.json.provider import JSONProvider


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


class LabManagerTypeEnum(EnumPython):
    PI = "Principal Investigator"
    CO_PI = "Co-Principal Investigator"
    LAB_MANAGER = "Lab Manager"
    POST_DOC = "Post Doctoral Researcher"
    GRAD_STUDENT = "Graduate Student"


class OrJSONProvider(JSONProvider):
    @staticmethod
    def dumps(obj, *, option=None, **kwargs):
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC
        if isinstance(obj, set):
            return orjson.dumps(list(obj), option=option).decode()
        return orjson.dumps(obj, option=option).decode()

    @staticmethod
    def loads(s, **kwargs):
        return orjson.loads(s)


def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    url_data = request.host_url + request.script_root
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host": request.host,
        "script_name": request.path,
        "server_port": url_data.split(":")[1] if ":" in url_data else "80",
        "get_data": request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        "post_data": request.form.copy(),
    }


def format_credits(credit_1, credit_2, credit_3, credit_4):
    # Create a list to hold the active credit numbers
    credits_output = []

    if credit_1:
        credits_output.append("1")
    if credit_2:
        credits_output.append("2")
    if credit_3:
        credits_output.append("3")
    if credit_4:
        credits_output.append("4")

    # Handle different cases
    if len(credits_output) == 4:
        return "1-4 Credits"
    elif len(credits_output) == 1:
        return (
            f"{credits_output[0]} Credit"
            if credit_1
            else f"{credits_output[0]} Credits"
        )
    elif credits_output == ["1", "2", "3"]:
        return "1-3 Credits"
    elif credits_output == ["2", "3", "4"]:
        return "2-4 Credits"
    elif len(credits_output) == 0:
        return None
    else:
        return f"{','.join(credits_output)} Credits"


def convert_to_enum(location_string) -> LocationEnum | None:
    try:
        return LocationEnum[
            location_string.upper()
        ]  # Use upper() for case-insensitivity
    except KeyError:
        return None  # Or raise an exception if you prefer
