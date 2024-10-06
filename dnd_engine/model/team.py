from typing import List

from dnd_engine.model.creature import Creature
from dnd_engine.model.entity import Entity


class Team(Entity):
    members: List[Creature]
    is_loser: bool = False
