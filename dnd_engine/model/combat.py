import random
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

from dnd_engine.model.creature import Creature
from dnd_engine.model.shared import EventModel
from dnd_engine.model.shared import ZeroPositiveInt
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
    queue: List[Creature] = []
    round: ZeroPositiveInt = 0
    owner: str
    status: str = "Not started"  # Not started -> Started -> Completed
    input_getter: Optional[Callable] = None

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

    def next_round(self):
        self.round += 1
        self.publish_event(f"Round {self.round}")

        for creature in self.queue:
            if self.is_completed():
                break
            if not creature.is_alive:
                continue

            actions = self.advice(creature)
            for action, target in actions:
                creature.apply(action, target)

    def advice_hp_based(
        self, myself: Creature, ap: int
    ) -> List[Tuple[Skill, Creature]]:
        target = self.get_target_for(myself)
        hp_left = int(round(100 * myself.hp / myself.max_hp, 0))
        actions = list()
        if hp_left < 50:
            actions.append((myself.get_skill_by_class("Move"), target))
        else:
            actions.append((myself.get_skill_by_class("Attack"), target))
        for _ in range(1, ap):
            actions.append((myself.get_skill_by_class("Attack"), target))
        return actions

    def advice_random(self, myself: Creature, ap: int) -> List[Tuple[Skill, Creature]]:
        target = self.get_target_for(myself)
        actions = list()
        for _ in range(ap):
            skill_name = str(random.choice(list(myself.skills.keys())))
            actions.append((myself.skills[skill_name], target))
        return actions

    def advice(self, myself: Creature, level: int = 1) -> List[Tuple[Skill, Creature]]:
        if isinstance(self.input_getter, Callable) and myself in self.teams[0].members:
            return self.input_getter(self, myself)

        # max_ap = myself.get_action_points()
        max_ap = 1

        if level == 0:  # Random choice
            return self.advice_random(myself, max_ap)

        if level == 1:  # HP based choice
            return self.advice_hp_based(myself, max_ap)

        raise AdviceNotFound
