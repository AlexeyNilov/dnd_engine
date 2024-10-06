from pydantic import BaseModel

from dnd_engine.model.entity import Entity


class Command(BaseModel):
    skill_name: str
    target: Entity
