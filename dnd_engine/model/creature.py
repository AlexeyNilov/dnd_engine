import logging
from typing import Callable
from typing import Dict
from typing import List

from pydantic import model_validator
from pydantic import PositiveInt

from dnd_engine.model.entity import Entity
from dnd_engine.model.event import publish_event
from dnd_engine.model.shared import GEZeroInt
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill import SkillTypeNotFound
from dnd_engine.model.skill_tech import get_skills_from_book
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)


class Creature(Entity):
    """Simple creature, see doc/creature.md for details"""

    is_alive: bool = True
    hp: GEZeroInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)
    skill_book: List[SkillRecord] = []
    skills: Dict[str, Skill] = {}
    compatible_with: List[str] = []
    reactions: Dict[str, Callable] = {}

    @model_validator(mode="after")
    def load_skills_from_skill_book(self):
        self.skills = get_skills_from_book(self.skill_book)
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        # React to changes
        if name in self.reactions.keys():
            self.reactions[name](self)

    def apply(self, skill: Skill, to: Entity) -> bool:
        """Apply given skill to the Entity if they are compatible, return False otherwise"""
        logger.debug(
            f"{self.id} {self.name} uses {skill.__class__.__name__}_level_{skill.level} on {to.id}"
        )

        if skill.__class__.__name__ in ["Consume"]:
            return use_consume_skill(creature=self, skill=skill, to=to)

        raise SkillTypeNotFound


def check_hp_above_zero(creature: Creature):
    if creature.is_alive and creature.hp <= 0:
        creature.is_alive = False
        creature.hp = 0
        publish_event(creature, "is dead")


def check_hp_less_than_max_hp(creature: Creature):
    if creature.hp > creature.max_hp:
        creature.hp = creature.max_hp
    if creature.hp == creature.max_hp:
        publish_event(creature, "is full")


def hp_tracker(creature: Creature):
    check_hp_less_than_max_hp(creature)
    check_hp_above_zero(creature)


default_reactions = {"hp": hp_tracker}


def use_consume_skill(creature: Creature, skill: Skill, to: Entity) -> bool:
    if to.nature not in creature.compatible_with:
        logger.debug(
            f"{skill.__class__.__name__} failed: {to.nature} is not compatible with {creature.name}"
        )
        return False

    if creature.hp == creature.max_hp:
        logger.debug(f"{creature.id} {creature.name} has max HP already")
        return False

    gain = skill.use(to)
    logger.debug(f"{creature.id} {creature.name} gained {gain} HP")
    if gain == 0:
        return False
    creature.hp += gain
    return True
