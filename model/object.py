from pydantic import BaseModel
from pydantic import Field
from typing_extensions import Annotated


GEZeroInt = Annotated[int, Field(ge=0)]


class ModelException(Exception):
    pass


class BaseObject(BaseModel):
    """ Simple object"""

    id: str  # Must be uniq globally
    name: str
