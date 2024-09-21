from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature
from model.creature import Creature
from model.skill import Consume


set_logging()
DB.clear()

data = {
    'name': 'hunter',
    'hp': 8,
    'max_hp': 10
}
save_creature(Creature(**data), DB)

data = {
    'name': 'prey',
    'hp': 4,
    'max_hp': 5,
    'skills': {
        'eat': Consume()
    },
    'compatible_with': ['organic'],
    'core': 'organic'
}
save_creature(Creature(**data), DB)

data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skills': {
        'drain': Consume()
    },
    'compatible_with': ['water'],
    'core': 'organic'
}
save_creature(Creature(**data), DB)

DB.close()
