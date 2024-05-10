from fastapi import APIRouter
from models.user import User

user_router = APIRouter(tags=["User"])

@user_router.post("/create")
async def create_user():
  new_user = User(name="vvv", password="asdf")
  await new_user.create()
  return new_user

@user_router.post("/login")
async def login():
  return {
    "message": "success"
  }

@user_router.get("/get")
async def get_user():
  user = await User.find_one(User.name == "vvv")
  return user

@user_router.get("/getAll")
async def get_all_user():
  users = await User.find_all().to_list()
  return {
    "response": users
  }