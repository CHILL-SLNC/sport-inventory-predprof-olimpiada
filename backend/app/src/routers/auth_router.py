from fastapi import APIRouter, HTTPException, status, Header
from src.auth import Auth
from src.queries.user_orm import AsyncUserORM
from src.queries.admin_orm import AsyncAdminORM
from src.schemas.user_schemas import UsersLoginDTO
from src.schemas.token_schemas import Token

auth_router = APIRouter()


@auth_router.post('/token', tags=["Авторизация"], summary="Получить токен")
async def login_for_access_token(user_data: UsersLoginDTO) -> Token:
    role = user_data.role
    password = user_data.password
    username = user_data.username
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if role == "user":
        hashed_password = await AsyncUserORM.get_password(username)
    elif role == "admin":
        hashed_password = await AsyncAdminORM.get_password(username)
    else:
        raise HTTPException(409, detail="Incorrect role")
    if Auth.verify_password(password, hashed_password):
        access_token = await Auth.create_access_token(username, role)
        return Token(access_token=access_token, token_type="bearer")
    raise credentials_exception


@auth_router.post('/get_role', tags=["Авторизация"], summary="Получить роль")
async def get_role(authorization: str = Header(...)) -> str:
    role = await Auth.get_role(authorization)
    return role


@auth_router.get('/role', tags=["Авторизация"], summary="Получить роль")
async def my_get_role(authorization: str = Header(...)) -> str:
    role = await get_role(authorization)
    return role


@auth_router.post('/get_username', tags=["Авторизация"], summary="Получить имя пользователя")
async def get_username(authorization: str = Header(...)) -> str:
    username = await Auth.get_username(authorization)
    return username
