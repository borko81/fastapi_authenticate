from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from fastapi import FastAPI, HTTPException, Query, Depends, status
from enum import Enum


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    heroes: list["Hero"] = Relationship(back_populates="team")


class NewTeam(SQLModel):
    name: str


class UpdateTeam(SQLModel):
    name: str | None = None


class ShowTeams(SQLModel):
    id: int
    name: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None
    team_id: int | None


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None


class HeroRead(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None = None
    team_id: int | None


class HeroSearchOptions(Enum):
    name = "name"
    secret_name = "secret_name"
    age = "age"


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# helpers function's
def get_row_from_table(
    id_: int,
    tablename: str,
    message="Not found that id :",
    session: Session = Depends(get_session),
):
    data = session.get(tablename, id_)
    if not data:
        raise HTTPException(status_code=404, detail=f"{message} {id_}")
    return data


# Team endpoint's
@app.post("/teams", response_model=ShowTeams, tags=["Team"])
def create_team(team: NewTeam, session: Session = Depends(get_session)):
    new_team = Team.model_validate(team)
    session.add(new_team)
    session.commit()
    session.refresh(new_team)
    return new_team


@app.get("/teams", response_model=list[ShowTeams], tags=["Team"])
def show_all_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@app.get("/team/{team_id}", response_model=ShowTeams, tags=["Team"])
def show_team_by_id(team_id: int, session: Session = Depends(get_session)):
    team = get_row_from_table(team_id, tablename=Team, session=session)
    return team


@app.patch("/team/{team_id}", response_model=ShowTeams, tags=["Team"])
def update_team(
    team_id: int, new_data: UpdateTeam, session: Session = Depends(get_session)
):
    team = get_row_from_table(team_id, tablename=Team, session=session)
    new_data = new_data.model_dump(exclude_unset=True)
    team.sqlmodel_update(new_data)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.delete("/team/{team_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Team"])
def delete_team_by_id(team_id: int, session: Session = Depends(get_session)):
    team = get_row_from_table(team_id, tablename=Team, session=session)
    session.delete(team)
    session.commit()
    return {"Status": "Success"}


# heroes endpoint's
@app.post("/heroes", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes", response_model=list[Hero])
def read_heroes(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.get("/heroes/from_name/{name}", response_model=list[HeroRead])
def read_hero_from_by_paramether(
    name: str,
    session: Session = Depends(get_session),
    q: HeroSearchOptions = HeroSearchOptions.name,
):
    mapper = {"name": Hero.name, "secret_name": Hero.secret_name}
    param = mapper.get(q.value)
    statement = select(Hero).where(param == name)
    result = session.exec(statement)
    return result


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    hero_id: int, hero: HeroUpdate, session: Session = Depends(get_session)
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_dat = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_dat)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(hero)
    session.commit()
    return {"Status": "Success"}
