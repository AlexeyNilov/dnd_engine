from pydantic import BaseModel
from pydantic import PositiveInt


class Creature(BaseModel):
    """ TBD
    """

    id: str
    name: str
    hp: PositiveInt  # Health points
    max_hp: PositiveInt  # TODO: make sure hp < max_hp
