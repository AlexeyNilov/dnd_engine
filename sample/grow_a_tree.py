from typing import List

from dnd_engine.data.fastite_loader import load_creature
from dnd_engine.data.logger import set_logging
from dnd_engine.model.event import Event
from dnd_engine.model.event import exec_on_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.resource import Resource


set_logging()

tree = load_creature(id="Creature_3")
tree.hp = tree.max_hp - 10
tree.events_publisher = publish_deque

water_data = {"name": "Water", "value": 200}
water = Resource(**water_data)

fruit_data = {"name": "Fruit", "value": 50}
fruits: List[Resource] = list()


def react(event: Event):
    if event.msg == "Full":
        fruit = Resource(**fruit_data)
        fruits.append(fruit)
        event.source.hp -= fruit.value


while water.value > 0:
    tree.hp -= 1
    tree.apply(skill=tree.skills["eat"], to=water)
    exec_on_deque(react)

assert len(fruits) == 3
assert tree.is_alive

print("Fruits created:", len(fruits))
print(tree.model_dump(include={"name", "hp", "max_hp", "is_alive", "skills"}))
