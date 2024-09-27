import logging

from pydantic import BaseModel
from pydantic import PositiveInt

from dnd_engine.model.shared import GEZeroInt

logger = logging.getLogger(__name__)


class SkillMethodNotImplemented(NotImplementedError):
    pass


class SkillTypeNotFound(NotImplementedError):
    pass


class SkillRecord(BaseModel):
    name: str
    skill_class: str
    used: GEZeroInt = 0
    level: PositiveInt = 1


# Fibonacci-based sequence
skill_upgrade_levels = {
    "2": 10,
    "3": 20,
    "4": 30,
    "5": 50,
    "6": 80,
    "7": 130,
    "8": 210,
    "9": 340,
    "10": 550,
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

    def use(self, *args, **kargs) -> int:
        raise SkillMethodNotImplemented

    # Track usage of skill
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr) and name == "use":
            self.__setattr__("used", self.used + 1)
        return attr

    # Level up skill
    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name == "used":
            new_level = calculate_level(self.used)
            if new_level > self.level:
                self.level = new_level
