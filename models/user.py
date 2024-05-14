from beanie import Document
from typing import Optional
from fastapi_users.db import BeanieBaseUser
from pydantic import BaseModel

class User(BeanieBaseUser, Document):
  name: str
  password: str
  partner_id: Optional[str] = None
  
class JoinUser(BaseModel):
  name: str
  email: str
  img: str
  

