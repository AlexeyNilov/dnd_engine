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


class AdviceNotFound(Exception):
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

    def advice_level_1(self, myself: Creature, ap: int) -> List[Skill]:
        hp_left = int(round(100 * myself.hp / myself.max_hp, 0))
        actions = list()
        if hp_left < 50:
            actions.append(myself.get_skill_by_class("Move"))
        else:
            actions.append(myself.get_skill_by_class("Attack"))
        for _ in range(1, ap):
            actions.append(myself.get_skill_by_class("Attack"))
        return actions

    def advice_random(self, myself: Creature, ap: int) -> List[Skill]:
        actions = list()
        for _ in range(ap):
            skill_name = str(random.choice(list(myself.skills.keys())))
            actions.append(myself.skills[skill_name])
        return actions

    def advice(self, myself: Creature, target: Creature, level: int = 1) -> List[Skill]:
        ap = myself.get_action_points()

        if level == 0:  # Random choice
            return self.advice_random(myself, ap)

        if level == 1:  # HP based choice
            return self.advice_level_1(myself, ap)

        options = myself.get_skill_classes()
        if len(options) == 1:
            actions: List[Skill] = []
            for _ in range(ap):
                actions.append(myself.get_skill_by_class(options[0]))
            return actions

        raise AdviceNotFound

    def battle(self):
        while not self.is_the_end():
            self.form_combat_queue()
            self.next_round()
            # break
