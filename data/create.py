from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature
from model.creature import Creature
from model.skill import Consume


set_logging()
DB.clear()

data = {
    'name': 'hunter',
    'hp': 10,
    'max_hp': 10
}
save_creature(Creature(**data), DB)

data = {
    'name': 'prey',
    'hp': 5,
    'max_hp': 5,
    'skills': {
        'eat': Consume()
    }
}
save_creature(Creature(**data), DB)

data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skills': {
        'drain': Consume()
    },
    'compatible_with': ['water']
}
save_creature(Creature(**data), DB)

DB.close()
