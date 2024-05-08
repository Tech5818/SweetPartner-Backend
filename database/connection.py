from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from models.oauth.google import GoogleOAuthUser, OAuthAccount
import logging
from dotenv import load_dotenv
import os
from fastapi_users.db import BeanieUserDatabase

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URL=os.getenv("MONGO_URL")

async def connect_mongodb():
  try:
    logger.info(" Connecting MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client["User"], document_models=[User, GoogleOAuthUser])
    logger.info(" Connect to MongoDB Successfully.")
  except :
    logger.error("Fail to connect MongoDB")

async def get_user_db():
  yield BeanieUserDatabase(GoogleOAuthUser, OAuthAccount)