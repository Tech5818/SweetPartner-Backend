from fastapi import APIRouter, Body, Request, Header, Depends, HTTPException
from models.user import User
from models.oauth.google import GoogleOAuthUser
from .auth.libs import get_jwt_strategy
from .auth.google import google_oauth_client
from jwt import decode, PyJWKClient

user_router = APIRouter(tags=["User"])

@user_router.post("/register")
async def register_user():
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
import os
from starlette.responses import RedirectResponse
@user_router.get("/verify")
async def verify_user(token: str = Depends(get_token)):
  url = "https://www.googleapis.com/oauth2/v3/certs"
  jwk_client = PyJWKClient(url)
  signing_key= jwk_client.get_signing_key_from_jwt(token)
  # payload = decode(token, "SECRET", algorithms="HS256", audience="AAA")
  payload = decode(token, signing_key.key, algorithms=["RS256"], audience=os.getenv("GOOGLE_OAUTH_ID"), issuer="https://accounts.google.com")
  
  print(payload)
  return RedirectResponse(url=f"http://localhost:5173?data={payload}")


@user_router.post("/login")
async def login(body:str):
  print(body)
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