from typing import List

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel


class Team(EventModel):
    members: List[Creature]
    is_loser: bool = False
    has_move: bool = False

    def remove_dead_members(self):
        self.members = [member for member in self.members if member.is_alive]

        if len(self.members) == 0:
            self.is_loser = True
            self.publish_event("Lost")
