from fastapi import FastAPI, Body
from model import PostSchema, PostsShow, UserLoginSchema, UserSchema
from auth.auth_handler import signJWT


app = FastAPI()

posts = [{"id": 1, "title": "Pancake", "content": "Lorem Ipsum ..."}]

users = []


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "welcome"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {"error": "No such content"}
    for post in posts:
        if post["id"] == id:
            return {"data": post}


@app.post("/posts", tags=["root"])
async def add_post(post: PostsShow) -> dict:
    post.id = len(posts) + 1
    posts.append(post.model_dump())
    return {"data": "post added successfully"}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Wrong login details"}
