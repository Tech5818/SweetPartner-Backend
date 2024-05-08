from beanie import Document
from typing import Optional
from fastapi_users.db import BeanieBaseUser

class User(BeanieBaseUser, Document):
  name: str
  password: str
  partner_id: Optional[str] = None
  