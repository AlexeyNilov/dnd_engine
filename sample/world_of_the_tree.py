import random
from typing import List

from dnd_engine.data import fastlite_loader as fl_loader
from dnd_engine.data.logger import set_logging
from dnd_engine.model.creature import Creature
from dnd_engine.model.event import Event
from dnd_engine.model.event import exec_on_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill_library import Consume


set_logging()

fl_loader.clear_events()
creatures = fl_loader.load_creatures()
head_count = 0
for creature in creatures:
    head_count += 1
    creature.events_publisher = publish_deque

resources: List[Resource] = []

water = {"name": "Water", "value": 50}
food = {"name": "Food", "value": 50}

for _ in range(10):
    resources.append(Resource(**water))
    resources.append(Resource(**food))


def remove_empty_resources():
    global resources
    resources = [r for r in resources if r.value > 0]


def remove_dead_creature(creature: Creature):
    global creatures
    fl_loader.delete_creature(creature)
    creatures.remove(creature)


def is_full(creature: Creature):
    global creatures
    global resources
    global head_count
    if creature == "Pig":
        start_hp = 20
        head_count += 1
        new_pig = Creature(
            id=f"Creature_{head_count}",
            name=f"Pig_{head_count}",
            skills={"eat": Consume()},
            hp=start_hp,
            max_hp=50,
            events_publisher=publish_deque,
        )
        creatures.append(new_pig)
        # creature.hp -= start_hp # TODO get creature by name

    if creature == "The first oak":
        new_food = Resource(**food)
        resources.append(new_food)
        # creature.hp -= new_food.value # TODO get creature by name

    if creature == "Wolf":
        pass
        # creature.max_hp *= 2 # TODO get creature by name


def is_dead(creature: Creature):
    global resources
    new_water = Resource(**water)
    resources.append(new_water)


def react(event: Event):
    global creatures
    global resources

    # Save to Events table
    fl_loader.save_event(event)

    if event.msg == "Full":
        is_full(event.source)

    if event.msg == "Died":
        is_dead(creature)


for _ in range(100):
    for creature in creatures:
        if not creature.is_alive:
            continue

        creature.hp -= 1  # Live sucks!

        if resources:
            resource = random.choice(resources)
            creature.do_by_class("Consume", resource)

        exec_on_deque(react)
        fl_loader.save_creature(creature)

for item in creatures:
    print(item.model_dump(include={"id", "name", "hp", "max_hp", "is_alive", "skills"}))

remove_empty_resources()
print(len(resources))
