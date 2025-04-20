from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.api.auth.auth_endpoints import register_new_user
from app.api.depends.depends import get_current_user
from app.api.models import AdminModel, UserModel
from app.core.database.crud import UserCrud

router = APIRouter(tags=['Admin'], prefix='/admins')

"""
Администратор должен иметь следующие возможности:
Авторизоваться по email/password
Получить данные о себе (id, email, full_name)
Создать/Удалить/Обновить пользователя
Получить список пользователей и список его счетов с балансами
"""

@router.post('/create_user')
async def create_user(user: Annotated[UserModel, Depends()], admin: Annotated[AdminModel, Depends(get_current_user)]):
    """Создаст нового пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await register_new_user(user=user)

@router.delete('/delete_user_by_id')
async def delete_user_by_id(user_id:int, admin: Annotated[AdminModel, Depends(get_current_user)]):
    """Удалит пользователя по id"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.delete_user_by_id(user_id=user_id)

@router.put('/update_user')
async def update_user(user_id: int, new_user: Annotated[UserModel, Depends()], admin: Annotated[AdminModel, Depends(get_current_user)]):
    """Полностью обновит пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.update_user(user_id=user_id, new_user=new_user)

@router.patch('/update_email')
async def update_user_email(new_email: EmailStr, old_email: EmailStr, admin: Annotated[AdminModel, Depends(get_current_user)]):
    """Обновит email пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.patch_email_user_for_admin(new_email=new_email, old_email=old_email)