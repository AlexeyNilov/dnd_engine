from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature


set_logging()

data = {
    'name': 'hunter',
    'hp': 10
}
save_creature(data, DB)

data = {
    'name': 'prey',
    'hp': 5
}
save_creature(data, DB)

data = {
    'name': 'tree',
    'hp': 500
}
save_creature(data, DB)

DB.close()
