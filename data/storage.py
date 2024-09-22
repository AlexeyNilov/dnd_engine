import logging
from typing import List

from sqlitedict import SqliteDict

from dnd_engine.model.creature import Creature


logger = logging.getLogger(__name__)
DB = SqliteDict("db.sqlite", autocommit=True)


class CreatureNotFound(Exception):
    pass


def save_creature(creature: Creature, db: SqliteDict) -> None:
    data = creature.model_dump()
    db[creature.id] = data
    logger.debug(f'{creature} saved')


def load_creatures(db: SqliteDict = DB) -> List[Creature]:
    creatures = list()
    for _, item in db.items():
        creatures.append(Creature(**item))
    return creatures


def get_creature(name: str, db: SqliteDict = DB) -> Creature:
    for _, item in db.items():
        if name == item['name']:
            return Creature(**item)
    raise CreatureNotFound
