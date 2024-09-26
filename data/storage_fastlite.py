import logging

import fastlite as fl
from sqlite_minutils.db import Database

from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)
DB: Database = fl.database("db/dnd.sqlite")


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        data = dict(skill_record_id=int, name=str, type=str, used=int, level=int, creature_id=str)
        skill_records.create(data, pk="skill_record_id")
    return skill_records


def get_skill_record(skill_record_id: int, db: Database = DB) -> SkillRecord:
    record = db.t.skill_records[skill_record_id]
    if record['used'] is None:
        record['used'] = 0
    if record['level'] is None:
        record['level'] = 1
    return SkillRecord(**record)


def set_skill_record(skill_record_id: int, creature_id: str, record: SkillRecord, db: Database = DB) -> dict:
    skill_records = db.t.skill_records
    data = record.model_dump()
    data["creature_id"] = creature_id
    data["skill_record_id"] = skill_record_id
    try:
        skill_records[data["skill_record_id"]]
    except fl.NotFoundError:
        return skill_records.insert(**data)
    else:
        return skill_records.update(**data)


def create_creatures_table(db=DB) -> fl.Table:
    table = db.t.creatures
    if table not in db.t:
        data = dict(creature_id=str, name=str, nature=str, is_alive=bool, hp=int, max_hp=int)
        table.create(data, pk="creature_id")
    return table
