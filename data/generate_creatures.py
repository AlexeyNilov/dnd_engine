from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature
from model.creature import Creature


set_logging()
DB.clear()

data = {
    'name': 'hunter',
    'hp': 8,
    'max_hp': 10,
    'skill_book': [
        ['eat', 'Consume', 1]
    ],
    'compatible_with': ['organic'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

data = {
    'name': 'prey',
    'hp': 4,
    'max_hp': 5,
    'skill_book': [
        ['eat', 'Consume', 1]
    ],
    'compatible_with': ['organic'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skill_book': [
        ['eat', 'Consume', 1]
    ],
    'compatible_with': ['water'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

DB.close()
