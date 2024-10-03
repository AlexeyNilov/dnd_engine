from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.service.battle import generate_teams


combat = Combat(
    name="Arena",
    events_publisher=publish_deque,
    teams=generate_teams(size=1, events_publisher=publish_deque),
    owner="Arena",
)
combat.form_combat_queue()
while not combat.is_completed():
    combat.next_round()

print_deque()
