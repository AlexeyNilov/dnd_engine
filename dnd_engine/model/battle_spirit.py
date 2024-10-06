from typing import Dict

from dnd_engine.model.combat import Combat
from dnd_engine.model.command import Command
from dnd_engine.model.creature import Creature
from dnd_engine.model.entity import Entity
from dnd_engine.model.skill import Skill


class BattleSpiritNotImplemented(NotImplementedError):
    pass


class BattleSpirit(Entity):
    creature: Creature
    combat: Combat
    skills: Dict[str, Skill] = {}

    def give_commands(self, *args, **kargs):
        raise BattleSpiritNotImplemented


class BiteSpirit(BattleSpirit):
    name: str = "BiteSpirit"

    def give_commands(self, *args, **kargs):
        commands = list()
        target = self.combat.get_target_for(self.creature)
        commands.append(Command(skill_name="bite", target=target))
        return commands
