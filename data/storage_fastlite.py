import logging

import fastlite as fl
from sqlite_minutils.db import Database

from dnd_engine.model.creature import Creature
from dnd_engine.model.skill_tech import get_skills_from_book
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)
DB: Database = fl.database("db/dnd.sqlite")


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        data = dict(
            skill_record_id=int,
            name=str,
            type=str,
            used=int,
            level=int,
            creature_id=str,
        )
        skill_records.create(data, pk="skill_record_id")
    return skill_records


def load_skill_record(skill_record_id: int, db: Database = DB) -> SkillRecord:
    record = db.t.skill_records[skill_record_id]
    if record["used"] is None:
        record["used"] = 0
    if record["level"] is None:
        record["level"] = 1
    return SkillRecord(**record)


def save_skill_record(
    skill_record_id: int, creature_id: str, record: SkillRecord, db: Database = DB
) -> dict:
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
        data = dict(
            creature_id=str,
            name=str,
            nature=str,
            is_alive=bool,
            hp=int,
            max_hp=int,
            compatible_with=str,
            reactions=str,
        )
        table.create(data, pk="creature_id")
    return table


def load_skill_book(creature_id: str, db: Database = DB) -> list:
    sql = f"SELECT skill_record_id FROM skill_records WHERE creature_id = '{creature_id}';"
    data = db.q(sql)
    skill_book = []
    for item in data:
        skill_book.append(
            load_skill_record(skill_record_id=item["skill_record_id"], db=db)
        )
    return skill_book


def load_creature(creature_id: int, db: Database = DB) -> Creature:
    c = db.t.creatures[creature_id]
    c["is_alive"] = bool(c["is_alive"])
    c["id"] = creature_id

    c.pop("nature", None)

    if c.get("compatible_with"):
        c["compatible_with"] = c["compatible_with"].split(";")

    c.pop("reactions", None)

    creature = Creature(**c)

    # Load skills
    skill_book = load_skill_book(creature_id=creature_id, db=db)
    if skill_book:
        creature.skills = get_skills_from_book(skill_book)

    return creature


def save_creature(creature: Creature, db: Database = DB) -> dict:
    ct = db.t.creatures
    data = creature.model_dump()
    data["creature_id"] = creature.id
    data["compatible_with"] = ";".join(data["compatible_with"])
    del data["id"]
    del data["skill_book"]

    for k, v in creature.skills.items():
        r = SkillRecord(name=k, type=v["type"], used=v["used"], level=v["level"])
        save_skill_record(skill_record_id=f"{creature.id}_{k}", creature_id=creature.id, record=r, db=db)
    del data["skills"]

    try:
        ct[data["creature_id"]]
    except fl.NotFoundError:
        return ct.insert(**data)
    else:
        return ct.update(**data)
