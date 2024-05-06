from fastapi import FastAPI
import uvicorn

from routes.user import user_router

from database.connection import connect_mongodb

app = FastAPI()

app.include_router(user_router, prefix="/user")

@app.on_event("startup")
async def on_startup():
  await connect_mongodb()

@app.get("/")
def home():
  return "home"


if __name__ == "__main__":
  uvicorn.run("main:app", host="localhost", port=8000, reload=True)
