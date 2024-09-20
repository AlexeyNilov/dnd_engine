from sqlitedict import SqliteDict

from model.creature import Creature


db = SqliteDict("db.sqlite", autocommit=True)

for _, item in db.items():
    print(Creature(**item))

db.close()
