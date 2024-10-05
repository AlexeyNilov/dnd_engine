import copy
import os
from functools import lru_cache
from typing import Callable
from typing import Dict

import yaml

from dnd_engine.model.creature import Creature
from dnd_engine.model.event import publish_deque
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill_library import SKILL_MAP


class CreatureNotFound(Exception):
    pass


@lru_cache
def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as fp:
        return yaml.safe_load(stream=fp)


BESTIARY_PATH = os.environ.get("BESTIARY_PATH", "db/bestiary.yaml")
BESTIARY = load_yaml(BESTIARY_PATH)


def get_skills(data: Dict[str, dict]) -> Dict[str, Skill]:
    bestiary_skills = {k: v for (k, v) in data.items()}
    skills: Dict[str, Skill] = {}
    for name, value in bestiary_skills.items():
        kargs = {"base": value["base"]}
        skills[name] = SKILL_MAP[value["type"]](**kargs)
    return skills


def get_creature(name: str, events_publisher: Callable = publish_deque) -> Creature:
    if name in BESTIARY:
        data = copy.deepcopy(BESTIARY[name])
        data["name"] = name
        data["events_publisher"] = events_publisher
        data["skills"] = get_skills(data["skills"])
        data["hp"] = data["max_hp"]
        return Creature(**data)
    raise CreatureNotFound
