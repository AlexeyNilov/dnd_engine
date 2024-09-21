from pydantic import BaseModel
from pydantic import model_validator
from pydantic import PositiveInt


class Creature(BaseModel):
    """ Simple creature """

    id: str
    name: str
    is_alive: bool
    hp: PositiveInt  # Health points
    max_hp: PositiveInt

    @model_validator(mode='after')
    def check_hp_less_than_max_hp(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'hp':
            self.check_hp_less_than_max_hp()


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
