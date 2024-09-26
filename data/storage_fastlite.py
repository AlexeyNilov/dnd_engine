import logging

import fastlite as fl

from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)
DB = fl.database("db/dnd.sqlite")


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        data = dict(id=int, name=str, type=str, used=int, level=int)
        skill_records.create(data, pk="id")
    return skill_records


def get_skill_record(id: int, db=DB) -> SkillRecord:
    skill_records = db.t.skill_records
    d = skill_records[id]
    if d['used'] is None:
        d['used'] = 0
    if d['level'] is None:
        d['level'] = 1
    return SkillRecord(**d)


# consume = SkillRecordDC(name="eat", type="consume")
# skill_records.insert(consume)
# print(skill_records())
