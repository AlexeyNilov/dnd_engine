import os
from functools import lru_cache

import yaml

from dnd_engine.model.creature import Creature


class CreatureNotFound(Exception):
    pass


@lru_cache
def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as fp:
        return yaml.safe_load(stream=fp)


def get_creature(name: str) -> Creature:
    path = os.environ.get("BESTIARY_PATH", "db/bestiary.yaml")
    db = load_yaml(path)
    if name in db:
        data = db[name]
        data["name"] = name
        return Creature(**data)
    raise CreatureNotFound
