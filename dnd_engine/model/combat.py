import random
from typing import List

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel
from dnd_engine.model.shared import ZeroPositiveInt
from dnd_engine.model.team import Team


class TargetNotFound(Exception):
    pass


class TeamNotFound(Exception):
    pass


class Combat(EventModel):
    teams: List[Team]
    queue: List[Creature] = []
    round: ZeroPositiveInt = 0
    status: str = "Not started"  # Not started -> Started -> Completed

    def is_completed(self) -> bool:
        if self.status == "Completed":
            return True
        for team in self.teams:
            if not all(m.is_alive for m in team.members):
                team.is_loser = True
                break
        if any(team.is_loser for team in self.teams):
            self.status = "Completed"
            self.publish_event(f"{team.name} lost")
            self.publish_event("The End")
            return True
        return False

    def form_combat_queue(self):
        self.status = "Started"
        self.queue = [member for team in self.teams for member in team.members]
        random.shuffle(self.queue)

    def get_team(self, creature: Creature) -> Team:
        team = next((team for team in self.teams if creature in team.members), None)
        if team is None:
            raise TeamNotFound
        return team

    def get_opposite_team(self, creature: Creature) -> Team:
        team = next((team for team in self.teams if creature not in team.members), None)
        if team is None:
            raise TeamNotFound
        return team

    def get_target_for(self, attacker: Creature) -> Creature:
        team = self.get_opposite_team(attacker)
        target = next((m for m in team.members if m.is_alive), None)
        if target:
            return target
        raise TargetNotFound
