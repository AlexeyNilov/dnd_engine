from pydantic import PositiveInt

from model.entity import Entity


class Resource(Entity):
    value: PositiveInt = 1
