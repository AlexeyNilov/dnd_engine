from typing import List

from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.command import Command
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_to_deque
from dnd_engine.service.team import generate_teams
from dnd_engine.service.team import prepare_teams


combat = Combat(
    name="Combat",
    events_publisher=publish_to_deque,
    teams=generate_teams(size=1),
    owner="Arena",
)


def get_input(creature: Creature) -> List[Command]:
    actions = list()
    target = combat.get_target_for(creature)
    actions.append(Command(skill_name="bite", target=target))
    return actions


prepare_teams(combat.teams, event_publisher=publish_to_deque, get_commands=get_input)

combat.start()

print_deque()
