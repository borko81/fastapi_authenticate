from fastapi import APIRouter
from model.creature import Creature
import fake.creature as service

router = APIRouter(prefix="/creature", tags=["creature"])


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature:
    return service.get_one(name)


@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("/")
def modify(id: int, creature: Creature) -> Creature:
    return service.modify(id, creature)


@router.put("/")
def replace(id: int, creature: Creature) -> Creature:
    return service.replace(id, creature)


@router.delete("/{name}")
def delete(id: int, name: str):
    return service.delete(name)
