from pydantic import BaseModel
from pydantic import model_validator
from pydantic import PositiveInt


class Creature(BaseModel):
    """ Simple creature """

    id: str
    name: str
    hp: PositiveInt  # Health points
    max_hp: PositiveInt

    @model_validator(mode='after')
    def check_hp_less_than_max_hp(self):  # TODO: test it
        if self.hp > self.max_hp:
            raise ValueError('hp must be less than max_hp')
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'hp':
            self.check_hp_less_than_max_hp()
