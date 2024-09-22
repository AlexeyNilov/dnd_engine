from data.logger import set_logging
from data.storage import DB
from data.storage import save_creature
from model.creature import Creature
from model.skill_tech import SkillRecord


set_logging()
DB.clear()

data = {
    'name': 'Wolf',
    'hp': 8,
    'max_hp': 10,
    'skill_book': [
        SkillRecord(name='eat', skill_class='Consume')
    ],
    'compatible_with': ['organic'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

data = {
    'name': 'Pig',
    'hp': 4,
    'max_hp': 5,
    'skill_book': [
        SkillRecord(name='eat', skill_class='Consume')
    ],
    'compatible_with': ['organic'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skill_book': [
        SkillRecord(name='eat', skill_class='Consume')
    ],
    'compatible_with': ['water'],
    'nature': 'organic'
}
save_creature(Creature(**data), DB)

DB.close()
