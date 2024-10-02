from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import PositiveInt

from dnd_engine.model.shared import ZeroPositiveInt
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill_library import Attack
from dnd_engine.model.skill_library import Consume
from dnd_engine.model.skill_library import Move


class SkillRecord(BaseModel):
    name: str
    type: str
    used: ZeroPositiveInt = 0
    level: PositiveInt = 1


available_skills = {"Consume": Consume, "Attack": Attack, "Move": Move}


def get_skills_from_book(skill_book: List[SkillRecord]) -> Dict[str, Skill]:
    skills: Dict[str, Skill] = {}
    for item in skill_book:
        skills[item.name] = available_skills[item.type](
            level=item.level, used=item.used
        )
    return skills
