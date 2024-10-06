import logging

import fastlite as fl
import pytest
from sqlite_minutils.db import NotFoundError

from dnd_engine.data import fastlite_db as fl_db
from dnd_engine.data import fastlite_loader as fl_loader
from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.creature import Creature
from dnd_engine.model.event import Event
from dnd_engine.model.skill_tech import SkillRecord
from dnd_engine.model.team import Team


logger = logging.getLogger(__name__)


@pytest.fixture
def team_red():
    return Team(name="Red", members=[get_creature("Wolf"), get_creature("Wolf")])


@pytest.fixture
def team_blue():
    return Team(name="Blue", members=[get_creature("Pig"), get_creature("Pig")])


@pytest.fixture
def combat(team_red, team_blue):
    c = Combat(name="Test", teams=[team_red, team_blue], owner="Test")
    c.form_combat_queue()
    return c


@pytest.fixture
def creature():
    return Creature(
        name="Test_Creature",
        hp=10,
        max_hp=20,
    )


@pytest.fixture
def empty_db():
    db = fl.database("db/test_empty.sqlite")
    for t in db.tables:
        t.drop()
    return db


@pytest.fixture
def filled_db():
    db = fl.database("db/test_filled.sqlite")
    fl_db.recreate_db(db)
    db.t.events.insert(source="Test_Creature_1", msg="test message")
    db.t.skill_records.insert(creature_id=1, name="eat", type="Consume")
    db.t.creatures.insert(name="Test_Creature", is_alive=True, hp=10, max_hp=100)
    db.t.actions.insert(id=1, attacker_id=0, target_id=1)
    return db


def test_create_actions_table(empty_db):
    table = fl_db.create_actions_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "actions"


def test_load_action(filled_db):
    assert fl_loader.load_action(1, filled_db) == {
        "attacker_id": 0,
        "id": 1,
        "target_id": 1,
        "skill_classes": None,
    }


def test_save_action(empty_db):
    fl_db.create_actions_table(empty_db)
    action = {"attacker_id": 0, "target_id": 1, "skill_classes": "Attack"}
    r = fl_loader.save_action(action, empty_db)
    del r["id"]
    assert r == action


def test_create_events_table(empty_db):
    table = fl_db.create_events_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "events"


def test_save_event(empty_db, creature):
    fl_db.create_events_table(empty_db)
    e = Event(source=creature.name, msg="test_message")
    r = fl_loader.save_event(e, db=empty_db)
    assert r == {"source": creature.name, "id": 1, "msg": "test_message"}


def test_load_events(filled_db):
    assert fl_loader.load_events(filled_db) == [
        {"source": "Test_Creature_1", "id": 1, "msg": "test message"}
    ]


def test_create_creatures_table(empty_db):
    table = fl_db.create_creatures_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "creatures"


def test_load_creature(filled_db):
    c = fl_loader.load_creature(id=1, db=filled_db)
    assert isinstance(c, Creature)
    assert c.name == "Test_Creature"
    assert isinstance(c.skills, dict)
    assert "eat" in c.skills.keys()


def test_create_skill_records_table(empty_db):
    table = fl_db.create_skill_records_table(empty_db)
    assert isinstance(table, fl.Table)
    assert table.name == "skill_records"


def test_load_skill_record(filled_db):
    r = fl_loader.load_skill_record(id="1", db=filled_db)
    assert isinstance(r, SkillRecord)
    assert r.used == 0
    assert r.level == 1


def test_save_skill_record_new(empty_db):
    fl_db.create_skill_records_table(empty_db)
    record = SkillRecord(name="test", type="consume")
    r = fl_loader.save_skill_record(creature_id=1, record=record, db=empty_db)
    assert r == {
        "id": 1,
        "level": 1,
        "name": "test",
        "type": "consume",
        "used": 0,
        "creature_id": 1,
    }


def test_delete_creature(empty_db, creature):
    fl_db.create_creatures_table(empty_db)
    fl_loader.save_creature(creature=creature, db=empty_db)
    fl_loader.delete_creature(creature=creature, db=empty_db)
    creature_id = creature.id
    with pytest.raises(NotFoundError):
        fl_loader.load_creature(id=creature_id, db=empty_db)


def test_save_creature(empty_db, creature):
    fl_db.create_creatures_table(empty_db)

    r = fl_loader.save_creature(creature=creature, db=empty_db)
    assert r == {
        "id": creature.id,
        "hp": 10,
        "is_alive": 1,
        "max_hp": 20,
        "name": "Test_Creature",
        "is_active": 0,
    }


def test_save_combat(empty_db, combat):
    fl_db.create_combats_table(empty_db)
    r = fl_loader.save_combat_view(combat=combat, db=empty_db)
    del r["queue"]
    assert r == {"name": "Test", "owner": None, "round": 0, "status": "Started"}
