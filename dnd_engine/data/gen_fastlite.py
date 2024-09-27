import fastlite as fl

from dnd_engine.data import storage_fastlite as sf
from dnd_engine.data.logger import set_logging
from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import DEFAULT_REACTIONS
from dnd_engine.model.skill_library import Consume


set_logging()
sf.DB.t.creatures.drop()
sf.create_creatures_table()
sf.DB.t.skill_records.drop()
sf.create_skill_records_table()

data = {
    "name": "Wolf",
    "hp": 40,
    "max_hp": 50,
    "skills": {"eat": Consume()},
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": DEFAULT_REACTIONS,
}
sf.save_creature(Creature(**data))


data = {
    "name": "Pig",
    "hp": 40,
    "max_hp": 50,
    "skills": {"eat": Consume()},
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": DEFAULT_REACTIONS,
}
sf.save_creature(Creature(**data))

data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skills": {"eat": Consume()},
    "compatible_with": ["water"],
    "nature": "organic",
    "reactions": DEFAULT_REACTIONS,
}
sf.save_creature(Creature(**data))

db = fl.database("db/dnd.sqlite")
for c in db.t.creatures():
    print(c)

for s in db.t.skill_records():
    print(s)
