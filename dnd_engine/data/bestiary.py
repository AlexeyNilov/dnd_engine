import os
from functools import lru_cache
from typing import Callable

import yaml

from dnd_engine.model.creature import Creature
from dnd_engine.model.event import publish_deque


class CreatureNotFound(Exception):
    pass


@lru_cache
def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as fp:
        return yaml.safe_load(stream=fp)


def get_creature(name: str, events_publisher: Callable = publish_deque) -> Creature:  # TODO Add skills
    path = os.environ.get("BESTIARY_PATH", "db/bestiary.yaml")
    db = load_yaml(path)
    if name in db:
        data = db[name]
        data["name"] = name
        data["events_publisher"] = events_publisher
        return Creature(**data)
    raise CreatureNotFound
