from typing import Dict, List, TypedDict

from pydantic.v1 import BaseModel, constr


class CoursesSpecOut(BaseModel):
    data: List[Dict[str, str]]


class CoursesSpecIn(BaseModel):
    input: constr(min_length=4)
