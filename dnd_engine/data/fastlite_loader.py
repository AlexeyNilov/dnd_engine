import logging
import os
from typing import List

import fastlite as fl
from sqlite_minutils.db import Database

from dnd_engine.data.fastlite_db import create_events_table
from dnd_engine.model.combat import Combat
from dnd_engine.model.creature import Creature
from dnd_engine.model.event import Event
from dnd_engine.model.skill_tech import get_skills_from_book
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)

db_path = os.environ.get("DB_PATH", "db/dnd.sqlite")
DB: Database = fl.database(db_path)


def clear_events(db: Database = DB):
    db.t.events.drop()
    create_events_table(db)


def save_event(event: Event, db: Database = DB) -> dict:
    events = db.t.events
    data = {"source": event.source, "msg": event.msg}

    return events.insert(**data)


def load_events(db: Database = DB) -> list:
    return db.t.events()


def load_skill_record(id: int, db: Database = DB) -> SkillRecord:
    record: dict = db.t.skill_records[id]
    record["used"] = 0 if record["used"] is None else record["used"]
    record["level"] = 1 if record["level"] is None else record["level"]
    return SkillRecord(**record)


def save_skill_record(creature_id: int, record: SkillRecord, db: Database = DB) -> dict:
    skill_records = db.t.skill_records
    data = record.model_dump()
    data["creature_id"] = creature_id

    sql = f"SELECT id FROM skill_records WHERE creature_id = {creature_id} AND name = {record.name};"
    try:
        sql_data = db.q(sql)
        data["id"] = sql_data[0]["id"]
        return skill_records.update(**data)
    except Exception:
        return skill_records.insert(**data)


def load_skill_book(creature_id: int, db: Database = DB) -> list:
    sql = f"SELECT id FROM skill_records WHERE creature_id = {creature_id};"
    data = db.q(sql)
    skill_book = []
    for item in data:
        skill_book.append(load_skill_record(id=item["id"], db=db))
    return skill_book


def del_none(d: dict):
    for k, v in d.items():
        if v is None:
            del d[k]
    return d


def convert_dict_to_creature(d: dict) -> Creature:
    d["is_alive"] = bool(d["is_alive"])
    d = del_none(d)
    return Creature(**d)


def load_creature(id: int, db: Database = DB) -> Creature:
    c = db.t.creatures[id]
    creature = convert_dict_to_creature(c)

    skill_book = load_skill_book(creature_id=id, db=db)
    if skill_book:
        creature.skills = get_skills_from_book(skill_book)

    return creature


def load_creatures(db: Database = DB) -> List[Creature]:
    creatures = []
    sql = "SELECT id FROM creatures;"
    data = db.q(sql)
    for item in data:
        creatures.append(load_creature(id=item["id"], db=db))

    return creatures


def delete_creature(creature: Creature, db: Database = DB) -> dict:
    ct = db.t.creatures
    return ct.delete(creature.id)


def save_creature(creature: Creature, db: Database = DB) -> dict:
    ct = db.t.creatures
    data = creature.model_dump()

    for k, skill in creature.skills.items():
        r = SkillRecord(
            name=k, type=skill.__class__.__name__, used=skill.used, level=skill.level
        )
        save_skill_record(creature_id=creature.id, record=r, db=db)

    for item in ["skills", "events_publisher"]:
        del data[item]

    return ct.upsert(**data)


def save_combat_view(combat: Combat, db: Database = DB) -> dict:
    queue_str = ""
    turn_map = {}
    turn = 0
    for creature in combat.queue:
        turn_map[creature.id] = turn
        turn += 1

    for team in combat.teams:
        for creature in team.members:
            queue_str += f"{team.name}:{creature.id}:{turn_map[creature.id]};"

    data = combat.model_dump()
    data["queue"] = queue_str
    for item in ["teams", "events_publisher"]:
        del data[item]
    ct = db.t.combats
    return ct.upsert(**data)
