from pydantic import BaseModel


class AccessTokenOnly(BaseModel):
    access_token: str
    token_type: str


class Token(AccessTokenOnly):
    ...


class TokenData(BaseModel):
    username: str | None = None
    role: str

