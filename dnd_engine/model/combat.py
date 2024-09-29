import random
from typing import List

from pydantic import PositiveInt

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel
from dnd_engine.model.team import Team


class TargetNotFound(Exception):
    pass


class Combat(EventModel):
    teams: List[Team]
    is_completed: bool = False
    queue: List[Creature] = []
    turn: PositiveInt = 1

    def is_the_end(self) -> bool:
        for team in self.teams:
            if team.is_loser:
                self.is_completed = True
                self.publish_event("The End")
                return True
        return False

    def form_combat_queue(self):
        self.queue = [member for team in self.teams for member in team.members]
        random.shuffle(self.queue)

    def get_target_for(self, attacker: Creature) -> Creature:
        for team in self.teams:
            if team.members and attacker not in team.members:
                return team.members[0]
        raise TargetNotFound

    def get_skill_name(self, creature: Creature) -> str:
        return str(random.choice(list(creature.skills.keys())))

    def fight(self):
        # Process creatures in the combat queue
        for creature in filter(lambda c: c.is_alive, self.queue):
            creature.do_by_name(self.get_skill_name(creature), self.get_target_for(creature))

        # Remove dead members from all teams
        [team.remove_dead_members() for team in self.teams]

    def battle(self):
        while not self.is_the_end():
            self.form_combat_queue()
            self.fight()
