from fastapi import APIRouter, Body, Request, Header, Depends, HTTPException
from models.user import User
from models.oauth.google import GoogleOAuthUser
from .auth.libs import get_jwt_strategy
from .auth.google import google_oauth_client
from jwt import decode

user_router = APIRouter(tags=["User"])

@user_router.post("/create")
async def create_user():
  new_user = User(name="vvv", password="asdf")
  await new_user.create()
  return new_user

def get_token(authorization: str = Header(...)):
  if not authorization:
    raise HTTPException(status_code=401, detail="Authorization Header가 없습니다.")
  if "bearer" not in authorization.lower():
    raise HTTPException(status_code=401, detail="Authorization 타입이 Berer이 아닙니다.")
  return authorization.split(" ")[1]

from bson import ObjectId
@user_router.get("/verify")
async def verify_user(token: str = Depends(get_token)):
  
  payload = decode(token, "SECRET", algorithms="HS256", audience="AAA")
  user_id = ObjectId(payload.get("sub"))
  user = await GoogleOAuthUser.find_one({"_id": user_id})
  print(user.email)
  print(type(user))
  return "hello"


@user_router.post("/login")
async def login(body = Body(...)):

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