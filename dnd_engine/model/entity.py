from threading import Lock
from typing import Any
from typing import ClassVar
from typing import Dict

from dnd_engine.model.shared import EventModel
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill import SkillNotFound


ID_COUNTER = 0


class Entity(EventModel):
    """See doc/entity.md for details"""

    id: int = 0  # Must be uniq globally
    skills: Dict[str, Skill] = {}

    _id_counter: ClassVar[int] = 0
    _lock: ClassVar[Lock] = Lock()

    def __init__(self, **data):
        if "id" not in data.keys() or data["id"] is None:
            with self._lock:
                data["id"] = self._get_next_id()
        super().__init__(**data)

    def _get_next_id(self) -> int:
        global ID_COUNTER
        ID_COUNTER += 1
        return ID_COUNTER

    def publish_event(self, msg: str):
        if callable(self.events_publisher):
            self.events_publisher(f"{self.name}_{self.id}", msg, self)

    def apply(self, skill_name: str, to: Any) -> bool:
        """Apply given skill to the Entity"""
        if skill_name not in self.skills.keys():
            raise SkillNotFound

        result = self.skills[skill_name].use(who=self, to=to)
        if hasattr(to, "id"):
            target = f"{to.name}_{to.id}"
        else:
            target = to.name

        self.publish_event(
            f"{skill_name.capitalize()} applied to {target} with result: {result}"
        )
        return bool(result)

    def get_action_points(self) -> int:
        return len(self.skills.keys())
