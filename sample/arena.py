from typing import List

from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.command import Command
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_to_deque
from dnd_engine.service.team import generate_teams


combat = Combat(
    name="Combat 1",
    events_publisher=publish_to_deque,
    teams=generate_teams(size=1),
    owner="Arena",
)


def get_input(creature: Creature) -> List[Command]:
    actions = list()
    target = combat.get_target_for(creature)
    actions.append(Command(skill_class="Attack", target=target))
    return actions


for team in combat.teams:
    team.events_publisher = publish_to_deque
    for m in team.members:
        m.events_publisher = publish_to_deque
        m.get_commands = get_input

combat.form_combat_queue()
while not combat.is_completed():
    combat.next_round()

print_deque()
