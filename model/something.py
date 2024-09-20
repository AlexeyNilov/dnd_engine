from pydantic import BaseModel
from pydantic import PositiveInt


class Something(BaseModel):
    """ TBD
    """

    id: str
    name: str
    hp: PositiveInt  # Health points
