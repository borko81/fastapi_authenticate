from model.explorer import Explorer


_explorers = [
    Explorer(name="Coala", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer | None:
    _explorer = [e for e in _explorers if e.name == name]
    try:
        return _explorer[0]
    except IndexError:
        return None


def create(explorer: Explorer) -> Explorer:
    return explorer


def modify(explorer: Explorer) -> Explorer:
    return explorer


def replace(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> bool:
    return None
