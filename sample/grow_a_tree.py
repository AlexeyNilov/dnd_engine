from typing import List

from data.logger import set_logging
from data.storage_fastlite import load_creature
from dnd_engine.model.event import Event
from dnd_engine.model.event import publish_event
from dnd_engine.model.event import start_event_manager
from dnd_engine.model.event import stop_event_manager
from dnd_engine.model.resource import Resource


set_logging()

tree = load_creature(creature_id="Creature_3")
tree.hp = tree.max_hp - 10
tree.events_publisher = publish_event

water_data = {"name": "Water", "value": 200, "nature": "water"}
water = Resource(**water_data)

fruit_data = {"name": "Fruit", "value": 50, "nature": "organic"}
fruits: List[Resource] = list()


def react(event: Event):
    if event.msg == "is full":
        fruit = Resource(**fruit_data)
        fruits.append(fruit)
        event.creature.hp -= fruit.value


thread = start_event_manager(func=react)

while water.value > 0:
    tree.hp -= 1
    tree.apply(skill=tree.skills["eat"], to=water)

stop_event_manager(thread)

print("Fruits created:", len(fruits))
print(tree.model_dump(include={"name", "hp", "max_hp", "is_alive", "skills"}))
