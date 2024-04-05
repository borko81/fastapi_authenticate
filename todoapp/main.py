from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session


from models import TodoDB
from database import engine, Base, SessionLocal
from schemas import TodoPut, ToDoRequest, ToDoResponse, TodoUpdate

from typing import Optional

# Configuration

app = FastAPI(title="Todo App")


# Database model
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# helpers function
def check_id_is_valid_in_db(id_: int, db: Session = Depends(get_db)):
    q = db.query(TodoDB).get(id_)
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found!")
    return q


# Ednpoint
@app.get("/todo", status_code=status.HTTP_200_OK, response_model=list[ToDoResponse])
async def root(db: Session = Depends(get_db), only: Optional[bool] = None):
    """Return all todo"""
    if only is not None:
        all_todos = db.query(TodoDB).filter(TodoDB.finished == only)
    else:
        all_todos = db.query(TodoDB).all()
    return all_todos


@app.post("/todo", status_code=status.HTTP_201_CREATED, response_model=ToDoResponse)
def create_new_todo(todo: ToDoRequest, db: Session = Depends(get_db)):
    new_todo = TodoDB(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.get("/todo/{id_}", status_code=status.HTTP_200_OK)
async def read_todo(id_: int, db: Session = Depends(get_db)):
    todo = check_id_is_valid_in_db(id_, db)
    return todo


@app.patch("/todo/{id_}", status_code=status.HTTP_202_ACCEPTED)
async def pach_todo(id_: int, update_todo: TodoUpdate, db: Session = Depends(get_db)):
    todo = check_id_is_valid_in_db(id_, db)
    new_value = update_todo.model_dump(exclude_unset=True)
    for key, value in new_value.items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todo/{id_}", status_code=status.HTTP_202_ACCEPTED)
async def put_todo(id_: int, update_todo: TodoPut, db: Session = Depends(get_db)):
    current_todo = check_id_is_valid_in_db(id_, db)
    current_todo = db.query(TodoDB).filter(TodoDB.id == id_)
    current_todo.update(update_todo.dict(), synchronize_session=False)

    db.commit()
    db.refresh(current_todo.first())
    return current_todo.first()


@app.delete("/todo/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id_: int, db: Session = Depends(get_db)):
    current_todo = check_id_is_valid_in_db(id_, db)
    db.delete(current_todo)
    db.commit()
    return None
