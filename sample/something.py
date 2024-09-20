from pydantic import BaseModel
from pydantic import PositiveInt


class Something(BaseModel):
    """ TBD
    """

    id: str
    name: str
    health_points: PositiveInt
