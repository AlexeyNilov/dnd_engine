from pydantic import BaseModel
from pydantic import PositiveInt

from model.object import Food
from model.object import GEZeroInt


class SkillMethodNotImplemented(NotImplementedError):
    pass


class Skill(BaseModel):
    description: str
    used: GEZeroInt = 0

    def use(self, *args, **kargs):
        self.used += 1
        raise SkillMethodNotImplemented


class ConsumeFood(Skill):
    description: str = 'Consume something with the given rate'
    rate: PositiveInt = 1

    def use(self, to: Food) -> int:
        self.used += 1
        if to.value <= 0:
            return 0

        gain = min(self.rate, to.value)
        to.value -= gain
        return gain
