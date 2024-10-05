from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Union


@dataclass
class Skill_Records:
    id: int | None = None
    name: str | None = None
    type: str | None = None
    used: int | None = None
    level: int | None = None
    creature_id: int | None = None


@dataclass
class Creatures:
    id: int | None = None
    name: str | None = None
    is_alive: int | None = None
    hp: int | None = None
    max_hp: int | None = None


@dataclass
class Events:
    id: int | None = None
    source: str | None = None
    msg: str | None = None


@dataclass
class Combats:
    name: str | None = None
    owner: str | None = None
    status: str | None = None
    round: int | None = None
    queue: str | None = None


@dataclass
class Actions:
    id: int | None = None
    attacker_id: int | None = None
    target_id: int | None = None
    skill_classes: str | None = None
