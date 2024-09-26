import logging

import fastlite as fl
import pytest

from data import storage_fastlite as sf
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    skill_records = db.t.skill_records
    if skill_records in db.t:
        skill_records.drop()
    return db


@pytest.fixture
def filled_db():
    db = fl.database("db/test_filled.sqlite")
    if 'skill_records' in db.t:
        db.t.skill_records.drop()
    skill_records = sf.create_skill_records_table(db)
    skill_records.insert(name="eat", type="consume")
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
