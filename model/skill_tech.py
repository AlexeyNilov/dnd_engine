from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import PositiveInt

from model.shared import GEZeroInt
from model.skill import Skill
from model.skill_library import Consume


class SkillRecord(BaseModel):
    name: str
    skill_class: str
    used: GEZeroInt = 0
    level: PositiveInt = 1


available_skills = {
    'Consume': Consume
}


def get_skills_from_book(skill_book: List[SkillRecord]) -> Dict[str, Skill]:
    skills: Dict[str, Skill] = {}
    for item in skill_book:
        skills[item.name] = available_skills[item.skill_class](level=item.level, used=item.used)
    return skills
