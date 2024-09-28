import logging

from pydantic import PositiveInt

from dnd_engine.model.creature import Creature
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill import Skill


logger = logging.getLogger(__name__)


class Consume(Skill):
    """Consume Resource entity with the given rate * skill level"""

    base_rate: PositiveInt = 1

    def use(self, to: Resource) -> int:
        if not isinstance(to, Resource):
            return 0

        effective_rate = self.base_rate * self.level
        if to.value <= 0:
            return 0

        gain = min(effective_rate, to.value)
        to.value -= gain
        return gain


class Attack(Skill):
    """ Attack another creature"""

    base_damage: PositiveInt = 1

    def use(self, to: Creature) -> int:
        if not isinstance(to, Creature):
            return 0

        effective_damage = self.base_damage * self.level
        if to.hp <= 0:
            return 0

        to.hp -= effective_damage
        return effective_damage
