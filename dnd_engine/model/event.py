from dnd_engine.model.entity import Entity


def publish_event(entity: Entity, msg: str) -> None:
    print(f"{entity.id} {entity.name}: {msg}")
