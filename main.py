from fastapi import FastAPI, Depends
import uvicorn

from routes.user import user_router

from database.connection import connect_mongodb

from routes.auth.google import google_oauth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    # "http://192.168.0.13:3000", # url을 등록해도 되고
    "*" # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)
app.include_router(user_router, prefix="/user")
app.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])

from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
)

import httpx
import os
from starlette.responses import RedirectResponse
from jwt import decode, PyJWKClient


@app.get("/callback")
async def auth(code: str):
  try:
     async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.googleapis.com/oauth2/v4/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": os.getenv("GOOGLE_OAUTH_ID"),
                "client_secret": os.getenv("GOOGLE_OAUTH_SECRET"),
                "redirect_uri": "http://localhost:8000/callback",
            },
        )
        print(response.json())
        response.raise_for_status()
        token_data = response.json()
        token = token_data["id_token"]
        
        url = "https://www.googleapis.com/oauth2/v3/certs"
        jwk_client = PyJWKClient(url)
        signing_key= jwk_client.get_signing_key_from_jwt(token)
        # payload = decode(token, "SECRET", algorithms="HS256", audience="AAA")
        payload = decode(token, signing_key.key, algorithms=["RS256"], audience=os.getenv("GOOGLE_OAUTH_ID"), issuer="https://accounts.google.com")
        
        print(payload)
        return RedirectResponse(url=f"http://localhost:5173?data={payload}")

  except Exception as e:
    print(e)
  

@app.get("/")
async def home():
  return "home"

@app.on_event("startup")
async def on_startup():
  await connect_mongodb()

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
