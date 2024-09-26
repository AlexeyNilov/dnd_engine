import logging

import fastlite as fl
import pytest

from data import storage_fastlite as sf
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    if "skill_records" in db.t:
        db.t.skill_records.drop()
    return db


@pytest.fixture
def filled_db():
    db = fl.database("db/test_filled.sqlite")
    if "skill_records" in db.t:
        db.t.skill_records.drop()
    skill_records = sf.create_skill_records_table(db)
    skill_records.insert(creature_id="Test_Creature_1", name="eat", type="consume")
    return db


def test_create_skill_records_table(empty_db):
    table = sf.create_skill_records_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "skill_records"


def test_get_skill_record(filled_db):
    r = sf.get_skill_record(id=1, db=filled_db)
    assert isinstance(r, SkillRecord)
    assert r.used == 0
    assert r.level == 1


def test_set_skill_record_new(empty_db):
    sf.create_skill_records_table(empty_db)
    record = SkillRecord(name="test", type="consume")
    r = sf.set_skill_record(id=1, creature_id="Test_Creature", record=record, db=empty_db)
    assert r == {"id": 1, "level": 1, "name": "test", "type": "consume", "used": 0, "creature_id": "Test_Creature"}
