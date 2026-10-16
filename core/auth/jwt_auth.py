from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt

from core.config import settings

security = HTTPBearer()

def get_authenticated_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
):
    return None

def generate_access_token(user_id: int, expires_in: int = 3600) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": now + timedelta(seconds=expires_in),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = 'HS256')

def generate_refresh_token(user_id: int, expires_in: int = 604800) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": now + timedelta(seconds=expires_in),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = 'HS256')