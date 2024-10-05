from typing import List

from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.command import Command
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.service.battle import generate_teams
from dnd_engine.service.battle import next_round


combat = Combat(
    name="Arena",
    events_publisher=publish_deque,
    teams=generate_teams(size=1),
    owner="Arena",
)


def get_input(creature: Creature) -> List[Command]:
    actions = list()
    target = combat.get_target_for(creature)
    actions.append(Command(skill_class="Attack", target=target))
    return actions


for team in combat.teams:
    for m in team.members:
        m.events_publisher = publish_deque
        m.get_commands = get_input

combat.form_combat_queue()
while not combat.is_completed():
    next_round(combat)

print_deque()
