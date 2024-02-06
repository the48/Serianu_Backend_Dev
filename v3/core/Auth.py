from core.Configs import settings
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt

from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def verify_password(plaintext_password):
    return pwd_context.verify(plaintext_password, settings.API_USER_PASSWORD)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    if (not username) or (username != settings.API_USER):
        return False
    if not verify_password(password):
        return False
    return username


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, algorithm = settings.JWT_ALGORITHM)
    return encoded_jwt