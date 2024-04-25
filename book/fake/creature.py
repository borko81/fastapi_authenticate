from model.creature import Creature
import data.creature as data


def get_all() -> list[Creature]:
    return data


def get_one(name: str) -> Creature | None:
    for _c in data:
        if _c.name == name:
            return _c
    return None


def create(creature: Creature) -> Creature:
    """Add a creature"""
    return creature


def modify(creature: Creature) -> Creature:
    """Partially modify a creature"""
    return data.modify(id, creature)


def replace(id: int, creature: Creature) -> Creature:
    """Completely replace a creature"""
    return data.replace(id, creature)


def delete(id: int, createure: Creature):
    """Delete a creature; return None if it existed"""
    return data.delete(id)
