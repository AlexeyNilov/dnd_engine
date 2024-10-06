from typing import List

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel


class Team(EventModel):
    members: List[Creature]
    is_loser: bool = False
