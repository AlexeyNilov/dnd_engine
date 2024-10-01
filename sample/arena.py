from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.team import Team


# Team Red
wolfs = [get_creature("Wolf") for _ in range(2)]
red = Team(name="Team Red", members=wolfs, events_publisher=publish_deque)

# Team Blue
pigs = [get_creature("Pig") for _ in range(2)]
blue = Team(name="Team Blue", members=pigs, events_publisher=publish_deque)

# Combat
combat = Combat(name="Arena", events_publisher=publish_deque, teams=[red, blue], owner="Arena")
combat.battle()

print_deque()

for wolf in wolfs:
    print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
for pig in pigs:
    print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
