from schemas import UserCreateSchema, UserListSchema
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
import models
import schemas


router = APIRouter()


def check_found_user_by_id(id_, db):
    user = db.query(models.User).filter(models.User.id == id_)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    q = db.query(models.User).all()
    return {"Status": "Success", "Count": len(q), "Users": q}


@router.get("/user/{id_}", status_code=status.HTTP_200_OK)
async def get_user_from_id(id_: int, db: Session = Depends(get_db)):
    user = check_found_user_by_id(id_, db)
    return {"Status": "Success", "User": user.first()}


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    payload: schemas.UserCreateSchema, db: Session = Depends(get_db)
):
    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Status": "Success", "NewUser": new_user}


@router.patch(
    "/user/{id_}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserUpdateSchema,
)
async def patch_user(
    id_: int, payload: schemas.UserUpdateSchema, db: Session = Depends(get_db)
):
    user = check_found_user_by_id(id_, db)

    user_update_data = payload.model_dump(exclude_unset=True)
    for key, value in user_update_data.items():
        setattr(user.first(), key, value)
    db.add(user.first())
    db.commit()
    db.refresh(user.first())
    return user.first()


@router.delete("/user/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_: int, db: Session = Depends(get_db)):
    user = check_found_user_by_id(id_, db)
    user.delete(synchronize_session=False)
    db.commit()
    return {"Status": "Success"}
