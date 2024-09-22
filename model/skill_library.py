from pydantic import PositiveInt

from model.resource import Resource
from model.skill import Skill


class Consume(Skill):
    """ Consume something with the given rate * skill level """
    rate: PositiveInt = 1

    def use(self, to: Resource) -> int:
        effective_rate = self.rate * self.level
        if to.value <= 0:
            return 0

        gain = min(effective_rate, to.value)
        to.value -= gain
        return gain
