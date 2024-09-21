from pydantic import BaseModel
from pydantic import PositiveInt


class Skill(BaseModel):
    description: str


class Consume(Skill):
    description: str = 'Consume something with the given rate'
    rate: PositiveInt = 1
