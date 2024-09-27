import logging

from pydantic import PositiveInt

from dnd_engine.model.resource import Resource
from dnd_engine.model.skill import Skill


logger = logging.getLogger(__name__)


class Consume(Skill):
    """Consume Resource entity with the given rate * skill level"""

    base_rate: PositiveInt = 1

    def use(self, to: Resource) -> int:
        if not isinstance(to, Resource):
            logger.error(
                f"Consume skill can be used only on Resource, tried on {type(to)}"
            )
            return 0

        effective_rate = self.base_rate * self.level
        if to.value <= 0:
            return 0

        gain = min(effective_rate, to.value)
        to.value -= gain
        return gain
