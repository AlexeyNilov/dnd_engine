import logging
from typing import Dict
from typing import List

from pydantic import model_validator
from pydantic import PositiveInt

from model.object import BaseObject
from model.object import GEZeroInt
from model.skill import available_skills
from model.skill import Skill


logger = logging.getLogger(__name__)


class Creature(BaseObject):
    """ Simple creature, see doc/creature.md for details"""

    is_alive: bool = True
    hp: GEZeroInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)
    skill_book: List[list] = []
    skills: Dict[str, Skill] = {}
    compatible_with: List[str] = []

    @model_validator(mode='after')
    def load_skills(self):
        for item in self.skill_book:
            self.skills[item[0]] = available_skills[item[1]](level=item[2])
        return self

    @model_validator(mode='after')
    def check_hp_less_than_max_hp(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self

    def check_hp_above_zero(self):
        if self.is_alive and self.hp <= 0:
            self.is_alive = False
            self.hp = 0
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'hp':
            self.check_hp_less_than_max_hp()
            self.check_hp_above_zero()

    def apply(self, what: Skill, to: BaseObject) -> None:
        logger.debug(f'{self.id} uses {what.__class__.__name__}_level_{what.level} on {to.id}')
        if to.core in self.compatible_with:
            gain = what.use(to)
            self.hp += gain
        else:
            logger.debug(f'{what.__class__.__name__} failed: {to.core} is not compatible with {self.name}')
