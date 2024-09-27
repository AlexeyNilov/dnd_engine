import logging
from typing import List

import fastlite as fl
from sqlite_minutils.db import Database

from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import get_tracker
from dnd_engine.model.shared import LockList
from dnd_engine.model.skill_tech import get_skills_from_book
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)
DB: Database = fl.database("db/dnd.sqlite")

skill_record_structure = dict(
    skill_record_id=str,
    name=str,
    type=str,
    used=int,
    level=int,
    creature_id=str,
)

creature_structure = dict(
    creature_id=str,
    name=str,
    nature=str,
    is_alive=bool,
    hp=int,
    max_hp=int,
    compatible_with=str,
    reactions=str,
)


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        skill_records.create(skill_record_structure, pk="skill_record_id")
    return skill_records


def load_skill_record(skill_record_id: int, db: Database = DB) -> SkillRecord:
    record: dict = db.t.skill_records[skill_record_id]
    record["used"] = 0 if record["used"] is None else record["used"]
    record["level"] = 1 if record["level"] is None else record["level"]
    return SkillRecord(**record)


def save_skill_record(creature_id: str, record: SkillRecord, db: Database = DB) -> dict:
    skill_records = db.t.skill_records
    data = record.model_dump()
    data["creature_id"] = creature_id
    data["skill_record_id"] = f"{creature_id}_{record.name}"

    return skill_records.upsert(**data)


def create_creatures_table(db=DB) -> fl.Table:
    table = db.t.creatures
    if table not in db.t:
        table.create(creature_structure, pk="creature_id")
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


def del_none(d: dict):
    for k, v in d.items():
        if v is None:
            del d[k]
    return d


def convert_dict_to_creature(d: dict) -> Creature:
    d["is_alive"] = bool(d["is_alive"])
    d["id"] = d["creature_id"]
    d["compatible_with"] = d.get("compatible_with", "none").split(";")

    if d.get("reactions"):
        d["reactions"] = {
            items[0]: get_tracker(items[1])
            for pair in d["reactions"].split(";")
            for items in [pair.split(":")]
        }

    d = del_none(d)
    return Creature(**d)


def load_creature(creature_id: str, db: Database = DB) -> Creature:
    c = db.t.creatures[creature_id]
    creature = convert_dict_to_creature(c)

    skill_book = load_skill_book(creature_id=creature_id, db=db)
    if skill_book:
        creature.skills = get_skills_from_book(skill_book)

    return creature


def load_creatures(db: Database = DB) -> List[Creature]:
    creatures = LockList()
    sql = "SELECT creature_id FROM creatures;"
    data = db.q(sql)
    for item in data:
        creatures.append(load_creature(creature_id=item["creature_id"], db=db))

    return creatures


def save_creature(creature: Creature, db: Database = DB) -> dict:
    ct = db.t.creatures
    data = creature.model_dump()
    data["creature_id"] = creature.id
    data["compatible_with"] = ";".join(data["compatible_with"])

    for k, skill in creature.skills.items():
        r = SkillRecord(
            name=k, type=skill.__class__.__name__, used=skill.used, level=skill.level
        )
        save_skill_record(creature_id=creature.id, record=r, db=db)

    for item in ["skills", "id", "events_publisher"]:
        del data[item]

    reactions = []
    for k, call in creature.reactions.items():
        reactions.append(f"{k}:{call.__name__}")
    data["reactions"] = ";".join(reactions)

    return ct.upsert(**data)
