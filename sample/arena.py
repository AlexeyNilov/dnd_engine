from typing import Dict

from dnd_engine.data.fastlite_loader import cleanup
from dnd_engine.model.battle_spirit import BattleSpirit
from dnd_engine.model.battle_spirit import BiteSpirit
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_to_deque
from dnd_engine.service.team import generate_teams


cleanup()

combat = Combat(
    name="Combat",
    events_publisher=publish_to_deque,
    teams=generate_teams(size=1),
    owner="Arena",
)

# Attach battle spirits
spirits: Dict[int, BattleSpirit] = {}
for team in combat.teams:
    for m in team.members:
        spirits[m.id] = BiteSpirit(
            creature=m, combat=combat, events_publisher=publish_to_deque
        )
        m.hp = m.max_hp
        m.events_publisher = publish_to_deque
        m.get_commands = spirits[m.id].give_commands


combat.start()
print_deque()
