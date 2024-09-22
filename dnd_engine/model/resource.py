from pydantic import PositiveInt

from dnd_engine.model.entity import Entity


class Resource(Entity):
    value: PositiveInt = 1
