import logging

from sqlitedict import SqliteDict

from model.creature import Creature


logger = logging.getLogger(__name__)
DB = SqliteDict("db.sqlite", autocommit=True)


class CreatureNotFound(Exception):
    pass


def save_creature(creature: Creature, db: SqliteDict) -> None:
    data = creature.model_dump()
    db[creature.id] = data
    logger.debug(f'{creature} saved')


def load_creatures(db: SqliteDict = DB) -> dict:
    creatures = dict()
    for _, item in db.items():
        creatures[item['id']] = Creature(**item)
    return creatures


def get_creature(name: str, db: SqliteDict = DB) -> Creature:
    for _, item in db.items():
        if name == item['name']:
            return Creature(**item)
    raise CreatureNotFound
