import logging
from typing import Dict
from typing import List

from pydantic import model_validator
from pydantic import PositiveInt

from model.object import BaseObject
from model.object import GEZeroInt
from model.skill import Consume


logger = logging.getLogger(__name__)


class Creature(BaseObject):
    """ Simple creature, see doc/creature.md for details"""

    is_alive: bool = True
    hp: GEZeroInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)
    skills: Dict[str, Consume] = {}
    compatible_with: List[str] = []

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

    def apply(self, what: Consume, to: BaseObject) -> None:
        logger.debug(f'{self.id} uses {what.__class__.__name__} level {what.level} on {to.id}')
        gain = what.use(to)
        self.hp += gain
