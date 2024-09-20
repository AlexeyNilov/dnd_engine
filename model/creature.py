from pydantic import BaseModel
from pydantic import PositiveInt


class Creature(BaseModel):
    """ TBD
    """

    id: str
    name: str
    hp: PositiveInt  # Health points
