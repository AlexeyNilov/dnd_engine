from sqlitedict import SqliteDict

from model.creature import Creature


db = SqliteDict("db.sqlite", autocommit=True)
last_id = 0


def save_creature(data: dict) -> None:
    global last_id
    data['id'] = str(last_id)
    last_id += 1
    creature = Creature(**data)
    print(creature, end='\t')
    data = creature.model_dump(mode='python')
    db[creature.id] = data
    print('saved')


data = {
    'name': 'hunter',
    'hp': 10
}
save_creature(data)

data = {
    'name': 'prey',
    'hp': 5
}
save_creature(data)

db.close()
