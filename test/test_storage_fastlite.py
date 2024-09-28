import logging

import fastlite as fl
import pytest

from dnd_engine.data import storage_fastlite as sf
from dnd_engine.model.creature import Creature
from dnd_engine.model.creature import DEFAULT_REACTIONS
from dnd_engine.model.event import Event
from dnd_engine.model.skill_tech import SkillRecord


logger = logging.getLogger(__name__)


@pytest.fixture
def creature():
    return Creature(
        name="test",
        hp=10,
        max_hp=20,
        compatible_with=["water"],
        reactions=DEFAULT_REACTIONS,
    )


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    if "skill_records" in db.t:
        db.t.skill_records.drop()
    if "creatures" in db.t:
        db.t.creatures.drop()
    if "events" in db.t:
        db.t.events.drop()
    return db


@pytest.fixture
def filled_db():
    db = fl.database("db/test_filled.sqlite")

    if "events" in db.t:
        db.t.events.drop()
    events = sf.create_events_table(db)
    events.insert(
        creature_id="Test_Creature_1", msg="test message"
    )

    if "skill_records" in db.t:
        db.t.skill_records.drop()
    skill_records = sf.create_skill_records_table(db)
    skill_records.insert(
        skill_record_id="1", creature_id="Test_Creature_1", name="eat", type="Consume"
    )

    if "creatures" in db.t:
        db.t.creatures.drop()
    creatures = sf.create_creatures_table(db)
    creatures.insert(
        creature_id="Test_Creature_1",
        name="Test_Creature",
        is_alive=True,
        hp=10,
        max_hp=100,
        compatible_with="water;organic",
        reactions="hp:hp_tracker",
        nature="organic"
    )
    return db


def test_create_events_table(empty_db):
    table = sf.create_events_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "events"


def test_save_event(empty_db, creature):
    sf.create_events_table(empty_db)
    e = Event(creature=creature, msg="test_message")
    r = sf.save_event(e, db=empty_db)
    assert r == {'creature_id': creature.id, 'id': 1, 'msg': 'test_message'}


def test_load_events(filled_db):
    assert sf.load_events(filled_db) == [{'creature_id': 'Test_Creature_1', 'id': 1, 'msg': 'test message'}]


def test_create_creatures_table(empty_db):
    table = sf.create_creatures_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "creatures"


def test_load_creature(filled_db):
    c = sf.load_creature(creature_id="Test_Creature_1", db=filled_db)
    assert isinstance(c, Creature)
    assert c.name == "Test_Creature"
    assert isinstance(c.skills, dict)
    assert "eat" in c.skills.keys()
    assert c.compatible_with == ["water", "organic"]
    assert "hp" in c.reactions.keys()
    assert c.nature == "organic"


def test_create_skill_records_table(empty_db):
    table = sf.create_skill_records_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "skill_records"


def test_load_skill_record(filled_db):
    r = sf.load_skill_record(skill_record_id="1", db=filled_db)
    assert isinstance(r, SkillRecord)
    assert r.used == 0
    assert r.level == 1


def test_save_skill_record_new(empty_db):
    sf.create_skill_records_table(empty_db)
    record = SkillRecord(name="test", type="consume")
    r = sf.save_skill_record(creature_id="Test_Creature", record=record, db=empty_db)
    assert r == {
        "skill_record_id": "Test_Creature_test",
        "level": 1,
        "name": "test",
        "type": "consume",
        "used": 0,
        "creature_id": "Test_Creature",
    }


def test_save_creature(empty_db, creature):
    sf.create_creatures_table(empty_db)

    r = sf.save_creature(creature=creature, db=empty_db)
    assert r == {
        "compatible_with": "water",
        "creature_id": creature.id,
        "hp": 10,
        "is_alive": 1,
        "max_hp": 20,
        "name": "test",
        "nature": "unknown",
        "reactions": "hp:hp_tracker",
    }
