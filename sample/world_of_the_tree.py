import random
from pprint import pprint
from typing import List

from data.logger import set_logging
from data.storage import load_creatures
from model.object import Resource


set_logging()

creatures = load_creatures()
resources: List[Resource] = list()

water = {
    'name': 'Water',
    'value': 20,
    'core': 'water'
}

food = {
    'name': 'Food',
    'value': 10,
    'core': 'organic'
}

for _ in range(5):
    resources.append(Resource(**water))
    resources.append(Resource(**food))


def remove_empty_resource():
    global resources
    for i, resource in enumerate(resources):
        if resource.value <= 0:
            resources.pop(i)


for _ in range(50):
    for creature in creatures:
        if resources:
            resource = random.choice(resources)
            creature.apply(what=creature.skills['eat'], to=resource)
        else:
            break

    remove_empty_resource()

for item in creatures:
    pprint(item.model_dump(include={'name', 'hp', 'max_hp', 'is_alive', 'skills'}))
