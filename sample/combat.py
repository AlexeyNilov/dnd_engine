from dnd_engine.data.storage_fastlite import load_creature
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill_library import Attack


wolf = load_creature(creature_id="Creature_1")
wolf.skills["attack"] = Attack(base_damage=100)
wolf.events_publisher = publish_deque

pig = load_creature(creature_id="Creature_2")
pig.events_publisher = publish_deque

wolf.do("Attack", pig)
print_deque()


print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
