from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature
from model.creature import create_creature


set_logging()

data = {
    'name': 'hunter',
    'hp': 10,
    'max_hp': 10
}
save_creature(create_creature(data), DB)

data = {
    'name': 'prey',
    'hp': 5,
    'max_hp': 5
}
save_creature(create_creature(data), DB)

data = {
    'name': 'tree',
    'hp': 500,
    'max_hp': 500
}
save_creature(create_creature(data), DB)

DB.close()
