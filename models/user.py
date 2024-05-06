from beanie import Document
from pydantic import Field
from bson import ObjectId
from typing import Optional

class User(Document):
  name: str = Field(...)
  password: str = Field(...)
  partnerId: Optional[ObjectId] = Field(None)
