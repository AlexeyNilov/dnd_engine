import logging
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from pydantic import PositiveInt

from dnd_engine.model.entity import Entity
from dnd_engine.model.shared import ConstrainedStr
from dnd_engine.model.shared import GEZeroInt
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill import SkillTypeNotFound


logger = logging.getLogger(__name__)


class Creature(Entity):
    """Simple creature, see doc/creature.md for details"""

    is_alive: bool = True
    hp: GEZeroInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)
    skills: Dict[str, Skill] = {}
    compatible_with: List[ConstrainedStr] = ["none"]
    events_publisher: Optional[Callable] = None

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        # React to changes
        if name == "hp":
            self.hp_tracker()

    def publish_event(self, msg: str):
        if callable(self.events_publisher):
            self.events_publisher(self, msg)

    def apply(self, skill: Skill, to: Entity) -> bool:
        """Apply given skill to the Entity"""
        if skill not in self.skills.values():
            raise SkillTypeNotFound

        result = skill.use(who=self, to=to)
        self.publish_event(
            f"{skill.__class__.__name__} applied to {to.name} with result: {result}"
        )
        return bool(result)

    def get_skill_by_class(self, skill_class: str) -> Skill:
        for skill in self.skills.values():
            if skill.__class__.__name__ == skill_class:
                return skill
        raise SkillTypeNotFound

    def do_by_class(self, skill_class: str, to: Entity) -> bool:
        return self.apply(skill=self.get_skill_by_class(skill_class), to=to)

    def do_by_name(self, skill_name: str, to: Entity) -> bool:
        return self.apply(skill=self.skills[skill_name], to=to)

    def check_hp_above_zero(self):
        if self.is_alive and self.hp <= 0:
            self.is_alive = False
            self.hp = 0
            self.publish_event("Died")

    def check_hp_less_than_max_hp(self):
        if self.hp == self.max_hp:
            self.publish_event("Full")

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def hp_tracker(self):
        self.check_hp_above_zero()
        if self.is_alive:
            self.check_hp_less_than_max_hp()
