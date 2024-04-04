from fastapi import FastAPI
import user
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, tags=["User"], prefix="/app/users")
