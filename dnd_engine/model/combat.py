import random
from typing import List

from pydantic import PositiveInt

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel
from dnd_engine.model.skill import Skill
from dnd_engine.model.team import Team


class TargetNotFound(Exception):
    pass


class TeamNotFound(Exception):
    pass


class Combat(EventModel):
    teams: List[Team]
    is_completed: bool = False
    queue: List[Creature] = []
    turn: PositiveInt = 1

    def is_the_end(self) -> bool:
        if any(team.is_loser for team in self.teams):
            self.is_completed = True
            self.publish_event("The End")
            return True
        return False

    def form_combat_queue(self):
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
        return self.get_opposite_team(attacker).members[0]

    def next_round(self):
        self.publish_event(f"Turn {self.turn}")

        # Process creatures in the combat queue
        for creature in filter(lambda c: c.is_alive, self.queue):
            actions = self.advice(creature, self.get_target_for(creature))
            for action in actions:
                creature.apply(action, self.get_target_for(creature))

        # Remove dead members from all teams
        [team.remove_dead_members() for team in self.teams]

        self.turn += 1

    def advice(self, myself: Creature, target: Creature, level: int = 1) -> List[Skill]:
        assert myself.skills

        ap = myself.get_action_points()
        print(f"I'm {myself.name}, I have {ap} action points")
        options = myself.get_skill_classes()
        print(f"I can: {options}")

        if len(options) == 1:
            print(f"I have no choice: {options[0]}")
            return [myself.get_skill_by_class(options[0])]

        if level == 0:  # Random choice
            skill_name = str(random.choice(list(myself.skills.keys())))
            print(f"I chose randomly: {myself.skills[skill_name].__class__.__name__}")
            return [myself.skills[skill_name]]

        if level == 1:  # HP based choice
            hp_left = int(round(100 * myself.hp / myself.max_hp, 0))
            print(f"I have {hp_left}% HP")
            if hp_left < 50:
                print("I chose to Move")
                return [myself.get_skill_by_class("Move")]

        print("I chose default: Attack")
        return [myself.get_skill_by_class("Attack")]

    def battle(self):
        while not self.is_the_end():
            self.form_combat_queue()
            self.next_round()
            # break
