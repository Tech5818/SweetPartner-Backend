from beanie import Document
from typing import Optional, List
from fastapi_users.db import BeanieBaseUser, BaseOAuthAccount
from pydantic import Field

class OAuthAccount(BaseOAuthAccount):
  pass
class GoogleOAuthUser(BeanieBaseUser, Document):
  oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
