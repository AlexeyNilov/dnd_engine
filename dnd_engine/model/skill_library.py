import logging
from typing import Callable
from typing import Dict

from dnd_engine.model.creature import Creature
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill import Skill


logger = logging.getLogger(__name__)


class Consume(Skill):
    """Consume Resource entity with the given rate * skill level"""
    def use(self, who: Creature, to: Resource) -> int:
        if not isinstance(to, Resource):
            return 0

        if to.nature not in who.compatible_with:
            return 0

        if who.hp == who.max_hp:
            return 0

        effective_rate = self.base * self.level
        if to.value <= 0:
            return 0

        gain = min(effective_rate, to.value)
        to.value -= gain
        who.hp += gain

        return gain


class Attack(Skill):
    """Attack creature"""
    def use(self, who: Creature, to: Creature) -> int:
        if not isinstance(to, Creature):
            return 0

        effective_damage = self.base * self.level
        if to.hp <= 0:
            return 0

        to.hp -= effective_damage
        return effective_damage


class Move(Skill):
    """Move creature"""
    def use(self, who: Creature, to: Creature) -> int:
        if not isinstance(to, Creature):
            return 0


SKILL_MAP: Dict[str, Callable] = {
    "Attack": Attack,
    "Consume": Consume,
    "Move": Move
}
