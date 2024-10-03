from typing import List
from typing import Tuple

from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill import Skill
from dnd_engine.service.battle import generate_teams


def get_input(combat: Combat, creature: Creature) -> List[Tuple[Skill, Creature]]:
    actions = list()
    target = combat.get_target_for(creature)
    skill = creature.get_skill_by_class("Attack")
    actions.append((skill, target))
    return actions


combat = Combat(
    name="Arena",
    events_publisher=publish_deque,
    teams=generate_teams(size=1, events_publisher=publish_deque),
    owner="Arena",
    input_getter=get_input,
)
combat.form_combat_queue()
while not combat.is_completed():
    combat.next_round()

print_deque()
