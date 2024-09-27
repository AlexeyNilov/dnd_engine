import random
from typing import List

from data.logger import set_logging
from data.storage_fastlite import load_creatures
from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import DEFAULT_REACTIONS
from dnd_engine.model.event import Event
from dnd_engine.model.event import exec_on_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill_library import Consume


set_logging()

creatures = load_creatures()
head_count = 0
for creature in creatures:
    head_count += 1
    creature.events_publisher = publish_deque

resources: List[Resource] = []

water = {"name": "Water", "value": 50, "nature": "water"}
food = {"name": "Food", "value": 50, "nature": "organic"}

for _ in range(10):
    resources.append(Resource(**water))
    resources.append(Resource(**food))


def remove_empty_resources():
    global resources
    for r in resources:
        if r.value <= 0:
            resources.remove(r)


def remove_dead_creature(creature: Creature):
    global creatures
    for c in creatures:
        if c.id == creature.id:
            creatures.remove(c)
            return


def is_full(creature: Creature):
    global creatures
    global resources
    global head_count
    if creature.name == "Pig":
        start_hp = 20
        head_count += 1
        new_pig = Creature(
            id=f"Creature_{head_count}",
            name="Pig",
            skills={"eat": Consume()},
            hp=start_hp,
            max_hp=50,
            events_publisher=publish_deque,
            reactions=DEFAULT_REACTIONS,
            nature="organic",
            compatible_with=["organic"]
        )
        creatures.append(new_pig)
        creature.hp -= start_hp

    if creature.name == "The first oak":
        new_food = Resource(**food)
        resources.append(new_food)
        creature.hp -= new_food.value

    if creature.name == "Wolf":
        creature.max_hp *= 2


def is_dead(creature: Creature):
    global resources
    new_water = Resource(**water)
    resources.append(new_water)
    remove_dead_creature(creature)


def react(event: Event):
    global creatures
    global resources

    # TODO save to Events table

    if event.msg == "is full":
        is_full(event.creature)

    if event.msg == "is dead":
        is_dead(creature)


for _ in range(100):
    for creature in creatures:
        if not creature.is_alive:
            continue

        creature.hp -= 1  # Live sucks!

        if resources:
            resource = random.choice(resources)  # TODO get compatible resource
            creature.apply(skill=creature.get_skill_by_class("Consume"), to=resource)

        exec_on_deque(react)

for item in creatures:
    print(item.model_dump(include={"id", "name", "hp", "max_hp", "is_alive", "skills"}))

remove_empty_resources()
print(len(resources))
