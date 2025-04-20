from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.api.models import UserModel
from app.api.depends.depends import get_current_user
from app.core.database.schemas import UserSchemas
from app.core.database.crud import UserCrud


router = APIRouter(tags=['User'], prefix='/users')


@router.get('/get_user_id')
async def get_user_id(user: Annotated[UserModel, Depends(get_current_user)]):
    """Вернет пользователя по id"""
    user = await UserCrud.get_user_id(email=user.email)
    return user if user else {'msg': 'user id not found'}

@router.get('/get_user_email')
async def get_user_email(user: Annotated[UserModel, Depends(get_current_user)]):
    """Вернет email пользователя"""
    return user.email

@router.get('/get_user_fullname')
async def get_user_fullname(user: Annotated[UserModel, Depends(get_current_user)]):
    """Вернет полное имя пользователя"""
    return {'fullname': f'{user.first_name} {user.last_name}'}

@router.patch('/update_email')
async def update_email(new_email: EmailStr, user: Annotated[UserModel, Depends(get_current_user)]):
    """Обновит email пользователя"""
    return await UserCrud.patch_email_user(new_email=new_email, old_email=user.email)

@router.patch('/update_password')
async def update_password(new_password: str, user: Annotated[UserModel, Depends(get_current_user)]):
    """Обновит password пользователя"""
    return await UserCrud.patch_password(new_password=new_password, email=user.email)