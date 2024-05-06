from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URL=os.getenv("MONGO_URL")

async def connect_mongodb():
  try:
    logger.info(" Connecting MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client["User"], document_models=[User])
    logger.info(" Connect to MongoDB Successfully.")
  except :
    logger.error("Fail to connect MongoDB")