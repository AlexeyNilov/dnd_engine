from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill_library import Attack
from dnd_engine.model.team import Team


# Team Red
wolf = get_creature("Wolf")
wolf.skills["attack"] = Attack(base_damage=2)
red = Team(name="Red", members=[wolf], events_publisher=publish_deque)

# Team Blue
pig = get_creature("Pig")
pig.skills["attack"] = Attack(base_damage=2)
blue = Team(name="Blue", members=[pig], events_publisher=publish_deque)

# Combat
combat = Combat(name="Arena", events_publisher=publish_deque, teams=[red, blue])
combat.battle()

print_deque()

print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
