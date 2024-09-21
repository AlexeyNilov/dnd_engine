from pydantic import BaseModel
# from pydantic import PositiveInt
# from typing import Optional


class BaseObject(BaseModel):
    """ Simple object"""

    id: str  # Must be uniq globally
    name: str
    # value: Optional[PositiveInt] = 1
