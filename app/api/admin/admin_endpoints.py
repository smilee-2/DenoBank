from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.api.auth.auth_endpoints import register_new_user
from app.api.depends.depends import get_current_user
from app.api.models import AdminModel, UserModel
from app.core.config.config import HTTP_BEARER
from app.core.database.crud import UserCrud, ScoreCrud

router = APIRouter(tags=['Admin'], prefix='/admins', dependencies=[Depends(HTTP_BEARER)])


@router.get('/user_with_scores')
async def get_user_scores(email: EmailStr, admin: Annotated[AdminModel, Depends(get_current_user)]) -> dict | None:
    """Получить список счетов с балансами пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await ScoreCrud.get_user_scores(email=email)


@router.get('/all_users')
async def get_all_users(admin: Annotated[AdminModel, Depends(get_current_user)]) -> list[UserModel]:
    """Получить список пользователей"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.get_all_users()


@router.post('/create_user')
async def create_user(user: Annotated[UserModel, Depends()],
                      admin: Annotated[AdminModel, Depends(get_current_user)]
                      ) -> dict[str, str]:
    """Создаст нового пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await register_new_user(user=user)


@router.delete('/delete_user_by_id')
async def delete_user_by_id(user_id: int, admin: Annotated[AdminModel, Depends(get_current_user)]) -> dict[str, str]:
    """Удалит пользователя по id"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.delete_user_by_id(user_id=user_id)


@router.put('/update_user')
async def update_user(user_id: int, new_user: Annotated[UserModel, Depends()],
                      admin: Annotated[AdminModel, Depends(get_current_user)]) -> dict[str, str] | None:
    """Полностью обновит пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.update_user(user_id=user_id, new_user=new_user)


@router.patch('/update_email')
async def update_user_email(new_email: EmailStr, old_email: EmailStr,
                            admin: Annotated[AdminModel, Depends(get_current_user)]) -> dict[str, str] | None:
    """Обновит email пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.patch_email_user_for_admin(new_email=new_email, old_email=old_email)


@router.patch('/disable_user')
async def disable_user(email: EmailStr,
                       admin: Annotated[AdminModel, Depends(get_current_user)]
                       ) -> dict[str, str] | None:
    """Заблокирует пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.disable_user(email=email)


@router.patch('/enable_user')
async def enable_user(email: EmailStr,
                      admin: Annotated[AdminModel, Depends(get_current_user)]
                      ) -> dict[str, str] | None:
    """Разблокирует пользователя"""
    if admin.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
    return await UserCrud.enable_user(email=email)
