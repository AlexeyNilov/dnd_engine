from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill_library import Attack


wolf = get_creature("Wolf")
wolf.skills["attack"] = Attack(base_damage=5)
wolf.events_publisher = publish_deque

pig = get_creature("Pig")
pig.events_publisher = publish_deque

wolf.do_by_name("attack", pig)
wolf.do_by_class("Attack", pig)
print_deque()


print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
