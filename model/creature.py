from pydantic import model_validator
from pydantic import PositiveInt

from model.object import BaseObject


class Creature(BaseObject):
    """ Simple creature, see doc/creature.md for details"""

    is_alive: bool
    hp: PositiveInt  # Health points (measure of aliveness)
    max_hp: PositiveInt  # Upper limit for health points (measure of growth)

    @model_validator(mode='after')
    def check_hp_less_than_max_hp(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self

    def check_hp_above_zero(self):
        if self.hp < 1:
            self.is_alive = False
            self.hp = 1  # HP looses its value when a creature is no longer alive and we set it to 1 to comply with PositiveInt
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'hp':
            self.check_hp_less_than_max_hp()
            self.check_hp_above_zero()


last_id = 0


def get_new_id() -> str:
    global last_id
    current_id = last_id
    last_id += 1
    return str(current_id)


def add_defaults(data: dict) -> dict:
    if 'id' not in data.keys():
        data['id'] = get_new_id()
    if 'is_alive' not in data.keys():
        data['is_alive'] = True

    return data


def create_creature(data: dict) -> Creature:
    data = add_defaults(data)
    return Creature(**data)
