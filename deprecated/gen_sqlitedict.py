from deprecated.storage_sqlite_dict import DB
from deprecated.storage_sqlite_dict import save_creature
from dnd_engine.model.creature import Creature
from dnd_engine.model.skill_tech import SkillRecord


DB.clear()

data = {
    "name": "Wolf",
    "hp": 16,
    "max_hp": 20,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["organic"],
    "nature": "organic",
}
save_creature(Creature(**data), DB)

data = {
    "name": "Pig",
    "hp": 8,
    "max_hp": 10,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["organic"],
    "nature": "organic",
}
save_creature(Creature(**data), DB)

data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["water"],
    "nature": "organic",
}
save_creature(Creature(**data), DB)

DB.close()
