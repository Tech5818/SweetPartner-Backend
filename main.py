from fastapi import FastAPI
import uvicorn

from routes.user import user_router

from database.connection import connect_mongodb

from routes.auth.google import google_oauth_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])

@app.on_event("startup")
async def on_startup():
  await connect_mongodb()

if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=8000, reload=True)
