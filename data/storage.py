import logging

from sqlitedict import SqliteDict

from model.creature import Creature


logger = logging.getLogger(__name__)
DB = SqliteDict("db.sqlite", autocommit=True)


def save_creature(creature: Creature, db: SqliteDict) -> None:
    data = creature.model_dump()
    db[creature.id] = data
    logger.debug(f'{creature} saved')


def load_creatures(db: SqliteDict = DB) -> dict:
    creatures = dict()
    for _, item in db.items():
        creatures[item['id']] = Creature(**item)
    return creatures
