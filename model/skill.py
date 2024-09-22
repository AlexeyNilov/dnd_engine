import logging

from pydantic import BaseModel
from pydantic import PositiveInt

from model.resource import Resource
from model.shared import GEZeroInt

logger = logging.getLogger(__name__)


class SkillMethodNotImplemented(NotImplementedError):
    pass


# Fibonacci-based sequence
skill_upgrade_levels = {
    '2': 10,
    '3': 20,
    '4': 30,
    '5': 50,
    '6': 80,
    '7': 130,
    '8': 210,
    '9': 340,
    '10': 550
}


def calculate_level(use: int) -> int:
    level = 1  # Default level
    for lvl, threshold in skill_upgrade_levels.items():
        if use >= threshold:
            level = int(lvl)
        else:
            break
    return level


class Skill(BaseModel):
    used: GEZeroInt = 0
    level: PositiveInt = 1

    def use(self, *args, **kargs):
        raise SkillMethodNotImplemented

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr) and name == "use":
            self.__setattr__('used', self.used + 1)
        return attr

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name == 'used':
            new_level = calculate_level(self.used)
            if new_level != self.level:
                logger.debug(f'{self.__class__.__name__} level changed from {self.level} to {new_level}')
            self.level = new_level


class Consume(Skill):
    """Consume something with the given rate * skill level"""
    rate: PositiveInt = 1

    def use(self, to: Resource) -> int:
        effective_rate = self.rate * self.level
        if to.value <= 0:
            return 0

        gain = min(effective_rate, to.value)
        to.value -= gain
        return gain


available_skills = {
    'Consume': Consume,
    'Skill': Skill
}
