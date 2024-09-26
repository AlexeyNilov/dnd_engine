import logging

import fastlite as fl
from sqlite_minutils.db import Database

from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)
DB: Database = fl.database("db/dnd.sqlite")


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        data = dict(id=int, name=str, type=str, used=int, level=int, creature_id=str)
        skill_records.create(data, pk="id")
    return skill_records


def get_skill_record(id: int, db: Database = DB) -> SkillRecord:
    record = db.t.skill_records[id]
    if record['used'] is None:
        record['used'] = 0
    if record['level'] is None:
        record['level'] = 1
    return SkillRecord(**record)


def set_skill_record(id: int, creature_id: str, record: SkillRecord, db: Database = DB) -> dict:
    skill_records = db.t.skill_records
    data = record.model_dump()
    data["creature_id"] = creature_id
    data["id"] = id
    try:
        skill_records[data["id"]]
    except fl.NotFoundError:
        return skill_records.insert(**data)
    else:
        return skill_records.update(**data)


def create_creatures_table(db=DB) -> fl.Table:
    table = db.t.creatures
    if table not in db.t:
        data = dict(id=str, name=str, type=str, used=int, level=int)
        table.create(data, pk="id")
    return table
