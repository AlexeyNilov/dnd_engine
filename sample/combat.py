from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill_library import Attack
from dnd_engine.model.team import Team


# Team Red
wolf = get_creature("Wolf")
wolf.skills["attack"] = Attack(base_damage=5)
wolf.events_publisher = publish_deque

red = Team(name="Red", members=[wolf])
red.events_publisher = publish_deque

# Team Blue
pig = get_creature("Pig")
pig.events_publisher = publish_deque

blue = Team(name="Blue", members=[pig])
blue.events_publisher = publish_deque

# Combat
wolf.do_by_name("attack", pig)
wolf.do_by_class("Attack", pig)
blue.remove_dead_members()
print_deque()


print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
