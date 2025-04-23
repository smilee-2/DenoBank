from typing import Annotated
from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from app.api.models import UserModel
from app.core.config.config import setting_access_token, setting_refresh_token
from app.core.database.crud import UserCrud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    """Вернет хеш пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Проверит пароль пользователя"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаст и вернет access jwt токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, setting_access_token.SECRET_KEY, algorithm=setting_access_token.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаст и вернет refresh jwt токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, setting_refresh_token.SECRET_KEY, algorithm=setting_refresh_token.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    """Проверит текущего пользователя"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, setting_access_token.SECRET_KEY, algorithms=[setting_access_token.ALGORITHM])
        type_token = payload.get('type')
        if type_token != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Bad token, get {type_token}, expected access')
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await UserCrud.get_user_by_email(email=email)

    if user is None:
        raise credentials_exception
    elif not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disabled')
    return user

async def get_current_user_for_refresh(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    """Проверит текущего пользователя по refresh"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, setting_access_token.SECRET_KEY, algorithms=[setting_access_token.ALGORITHM])
        type_token = payload.get('type')
        if type_token != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Bad token, get {type_token}, expected refresh')
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await UserCrud.get_user_by_email(email=email)

    if user is None:
        raise credentials_exception
    elif not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disabled')
    return user

if __name__ == '__main__':
    print(get_password_hash('1115509d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'))