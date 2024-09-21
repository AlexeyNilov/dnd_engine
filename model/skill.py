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
        raise SkillMethodNotImplemented

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr) and name == "use":
            self.__setattr__('used', self.used + 1)
            # TODO implement skill upgrade

        return attr


class ConsumeFood(Skill):
    description: str = 'Consume something with the given rate'
    rate: PositiveInt = 1

    def use(self, to: Food) -> int:
        if to.value <= 0:
            return 0

        gain = min(self.rate, to.value)
        to.value -= gain
        return gain
