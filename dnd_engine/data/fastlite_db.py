import os
from typing import Callable
from typing import Dict

import fastlite as fl
from sqlite_minutils.db import Database


db_path = os.environ.get("DB_PATH", "db/dnd.sqlite")
DB: Database = fl.database(db_path)


skill_record_structure = dict(
    id=int,
    name=str,
    type=str,
    used=int,
    level=int,
    creature_id=int,
)

creature_structure = dict(
    id=int, name=str, is_alive=bool, hp=int, max_hp=int, is_active=bool
)

combat_structure = dict(
    name=str,
    owner=str,
    status=str,
    round=int,
    queue=str,
)

action_structure = dict(id=int, attacker_id=int, target_id=int, skill_names=str)

event_structure = dict(id=int, source=str, msg=str)


def create_actions_table(db=DB) -> fl.Table:
    actions = db.t.actions
    if actions not in db.t:
        actions.create(action_structure, pk="id")
    return actions


def create_events_table(db=DB) -> fl.Table:
    events = db.t.events
    if events not in db.t:
        events.create(event_structure, pk="id")
    return events


def create_skill_records_table(db=DB) -> fl.Table:
    skill_records = db.t.skill_records
    if skill_records not in db.t:
        skill_records.create(skill_record_structure, pk="id")
    return skill_records


def create_creatures_table(db=DB) -> fl.Table:
    table = db.t.creatures
    if table not in db.t:
        table.create(creature_structure, pk="id")
    return table


def create_combats_table(db=DB) -> fl.Table:
    table = db.t.combats
    if table not in db.t:
        table.create(combat_structure, pk="name")
    return table


TABLES: Dict[str, Callable] = {
    "skill_records": create_skill_records_table,
    "creatures": create_creatures_table,
    "events": create_events_table,
    "combats": create_combats_table,
    "actions": create_actions_table,
}


def recreate_db(db: Database = DB):
    for t in db.tables:
        t.drop()

    for create_func in TABLES.values():
        create_func(db)
