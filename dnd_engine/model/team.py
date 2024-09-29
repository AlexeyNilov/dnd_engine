from typing import Callable
from typing import List
from typing import Optional

from pydantic import BaseModel

from dnd_engine.model.creature import Creature


class Team(BaseModel):
    name: str
    members: List[Creature]
    is_loser: bool = False
    has_move: bool = False
    events_publisher: Optional[Callable] = None

    def publish_event(self, msg: str):
        if callable(self.events_publisher):
            self.events_publisher(self, msg)

    def remove_dead_members(self):
        self.members = [member for member in self.members if member.is_alive]

        if len(self.members) == 0:
            self.is_loser = True
            self.publish_event("Lost")
