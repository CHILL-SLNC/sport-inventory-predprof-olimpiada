from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from src.config import settings
from src.schemas.token_schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
access_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class Auth():
    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def create_access_token(username: str, role: str,
                                  expires_delta: timedelta | None = timedelta(minutes=access_expires)) -> str:
        to_encode = {"username": username, "role": role}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("username")
            role: str = payload.get("role")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username, role=role)
        except InvalidTokenError:
            raise credentials_exception
        return token_data

    @staticmethod
    async def get_role(authorization: str = Header(...)) -> str:
        if not authorization:
            raise HTTPException(status_code=400, detail="Authorization header missing")
        type, token = authorization.split(' ')
        token_data = await Auth.decode_access_token(token)
        return token_data.role

    @staticmethod
    async def get_username(authorization: str = Header(...)) -> str:
        if not authorization:
            raise HTTPException(status_code=400, detail="Authorization header missing")
        type, token = authorization.split(' ')
        token_data = await Auth.decode_access_token(token)
        return token_data.username
