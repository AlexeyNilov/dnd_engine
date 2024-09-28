from dnd_engine.data import storage_fastlite as sf
from dnd_engine.model.creature import Creature
from dnd_engine.model.skill_library import Consume


sf.DB.t.creatures.drop()
sf.create_creatures_table()
sf.DB.t.skill_records.drop()
sf.create_skill_records_table()
sf.DB.t.events.drop()
sf.create_events_table()

data = {
    "name": "Wolf",
    "hp": 40,
    "max_hp": 50,
    "skills": {"eat": Consume()},
    "compatible_with": ["organic"],
    "nature": "organic",
}
sf.save_creature(Creature(**data))


data = {
    "name": "Pig",
    "hp": 40,
    "max_hp": 50,
    "skills": {"eat": Consume()},
    "compatible_with": ["organic"],
    "nature": "organic",
}
sf.save_creature(Creature(**data))

data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skills": {"eat": Consume()},
    "compatible_with": ["water"],
    "nature": "organic",
}
sf.save_creature(Creature(**data))

for c in sf.DB.t.creatures():
    print(c)

for s in sf.DB.t.skill_records():
    print(s)
