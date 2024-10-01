from dnd_engine.data.bestiary import get_creature
from dnd_engine.data.fastlite_loader import save_combat_view
from dnd_engine.data.fastlite_loader import save_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.team import Team


# Team Red
wolfs = [get_creature("Wolf") for _ in range(2)]
for wolf in wolfs:
    save_creature(wolf)
red = Team(name="Team Red", members=wolfs, events_publisher=publish_deque)

# Team Blue
pigs = [get_creature("Pig") for _ in range(2)]
blue = Team(name="Team Blue", members=pigs, events_publisher=publish_deque)
for pig in pigs:
    save_creature(pig)

# Combat
combat = Combat(name="Arena", events_publisher=publish_deque, teams=[red, blue], owner="Arena")
combat.status = "Started"
while not combat.is_the_end():
    combat.form_combat_queue()
    combat.next_round()
    save_combat_view(combat)
    break
combat.status = "Completed"

print_deque()

for wolf in wolfs:
    print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
for pig in pigs:
    print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
