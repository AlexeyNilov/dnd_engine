from data.logger import set_logging
from data.storage_sqlite_dict import DB
from data.storage_sqlite_dict import save_creature
from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import default_reactions
from dnd_engine.model.skill_tech import SkillRecord


set_logging()
DB.clear()

data = {
    "name": "Wolf",
    "hp": 16,
    "max_hp": 20,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": default_reactions
}
save_creature(Creature(**data), DB)

data = {
    "name": "Pig",
    "hp": 8,
    "max_hp": 10,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["organic"],
    "nature": "organic",
    "reactions": default_reactions
}
save_creature(Creature(**data), DB)

data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skill_book": [SkillRecord(name="eat", type="Consume")],
    "compatible_with": ["water"],
    "nature": "organic",
    "reactions": default_reactions
}
save_creature(Creature(**data), DB)

DB.close()
