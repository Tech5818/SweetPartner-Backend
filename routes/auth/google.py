from httpx_oauth.clients.google import GoogleOAuth2
from fastapi_users.router.oauth import get_oauth_router
from .libs import auth_backend, SECRET
from .manager import get_user_manager
import os

google_oauth_client = GoogleOAuth2(
  client_id=os.getenv("GOOGLE_OAUTH_ID"),
  client_secret=os.getenv("GOOGLE_OAUTH_SECRET"),
  scopes=[
    "https://www.googleapis.com/auth/userinfo.profile", # 구글 클라우드에서 설정한 scope
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
  ],
)

google_oauth_router = get_oauth_router(
  oauth_client=google_oauth_client,
  get_user_manager=get_user_manager,
  backend=auth_backend,
  state_secret=SECRET,
  redirect_url="http://localhost:8000/auth/google/callback",
  # associate_by_email=True
)
