from typing import Callable
from typing import List
from typing import Optional

from pydantic import PositiveInt

from dnd_engine.model.command import Command
from dnd_engine.model.entity import Entity
from dnd_engine.model.shared import ZeroPositiveInt


class Creature(Entity):
    """Simple creature, see doc/creature.md for details"""

    is_alive: bool = True
    hp: ZeroPositiveInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)
    get_commands: Optional[Callable] = None
    is_active: bool = False  # Has turn

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        # React to changes
        if name == "hp":
            self.hp_tracker()

    def act(self) -> None:
        self.is_active = True
        self.publish_event("It's my turn")
        if callable(self.get_commands):
            commands: List[Command] = self.get_commands(self)
            ap = min(self.get_action_points(), len(commands))
            for command in commands[:ap]:
                self.apply(command.skill_name, to=command.target)
        self.is_active = False
        self.publish_event("Completed my turn")

    def check_hp_above_zero(self):
        if self.is_alive and self.hp <= 0:
            self.is_alive = False
            self.hp = 0
            self.publish_event("I'm dead")

    def check_hp_less_than_max_hp(self):
        if self.hp == self.max_hp:
            self.publish_event("I'm full")

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def hp_tracker(self):
        self.check_hp_above_zero()
        if self.is_alive:
            self.check_hp_less_than_max_hp()
            self.publish_event("My HP changed")
