from fastapi import APIRouter
from models.user import User
from database.connection import connect_mongodb

user_router = APIRouter(tags=["User"])

@user_router.post("/create")
async def create_user():
  connect_mongodb()
  new_user = User(name="aaa", password="asdf")
  await new_user.create()
  return new_user