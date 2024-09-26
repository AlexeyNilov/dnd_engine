from pprint import pprint

import fastlite as fl

from data import storage_fastlite as sf
from data.logger import set_logging
from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import default_reactions
from dnd_engine.model.skill_library import Consume
from dnd_engine.model.skill_tech import SkillRecord


set_logging()
sf.create_creatures_table()
sf.create_skill_records_table()

data = {
    "name": "Wolf",
    "hp": 16,
    "max_hp": 20,
    "skills": {"eat": Consume()},
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": default_reactions,
}
c = Creature(**data)
sf.save_creature(c)

exit()

data = {
    "name": "Pig",
    "hp": 8,
    "max_hp": 10,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": default_reactions,
}
sf.save_creature(Creature(**data))

data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["water"],
    "nature": "organic",
    "reactions": default_reactions,
}
sf.save_creature(Creature(**data))

db = fl.database("db/dnd.sqlite")
t = db.t.creatures
pprint(t())

t = db.t.skill_records
pprint(t())
