import random
from pprint import pprint
from typing import List

from data.logger import set_logging
from data.storage_fastlite import load_creatures
from dnd_engine.model.resource import Resource


set_logging()

creatures = load_creatures()
resources: List[Resource] = list()

water = {"name": "Water", "value": 20, "nature": "water"}
food = {"name": "Food", "value": 20, "nature": "organic"}

for _ in range(20):
    resources.append(Resource(**water))
    resources.append(Resource(**food))


def remove_empty_resource():
    global resources
    for i, resource in enumerate(resources):
        if resource.value <= 0:
            resources.pop(i)


for _ in range(50):
    for creature in creatures:
        if not creature.is_alive:
            continue

        creature.hp -= 1  # Live sucks!

        if resources:
            resource = random.choice(resources)
            creature.apply(skill=creature.get_skill_by_class("Consume"), to=resource)
            remove_empty_resource()


for item in creatures:
    pprint(item.model_dump(include={"name", "hp", "max_hp", "is_alive", "skills"}))
