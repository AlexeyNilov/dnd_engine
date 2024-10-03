from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.service.battle import generate_teams


# Combat
combat = Combat(
    name="Arena",
    events_publisher=publish_deque,
    teams=generate_teams(size=2, events_publisher=publish_deque),
    owner="Arena",
)
combat.status = "Started"
combat.form_combat_queue()
while not combat.is_the_end():
    combat.next_round()
    # break

combat.status = "Completed"

print_deque()
