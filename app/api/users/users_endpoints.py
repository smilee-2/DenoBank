from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.api.models import UserModel
from app.api.depends.depends import get_current_user
from app.core.database.schemas import UserSchemas
from app.core.database.crud import UserCrud, ScoreCrud

router = APIRouter(tags=['User'], prefix='/users')


@router.get('/get_user_id')
async def get_user_id(user: Annotated[UserModel, Depends(get_current_user)]) -> int | None:
    """Вернет пользователя по id"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    user = await UserCrud.get_user_id(email=user.email)
    return user if user else {'msg': 'user id not found'}


@router.get('/get_user_email')
async def get_user_email(user: Annotated[UserModel, Depends(get_current_user)]) -> EmailStr:
    """Вернет email пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return user.email


@router.get('/get_user_fullname')
async def get_user_fullname(user: Annotated[UserModel, Depends(get_current_user)]) -> dict[str, str]:
    """Вернет полное имя пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return {'fullname': f'{user.first_name} {user.last_name}'}


@router.patch('/update_email')
async def update_email(new_email: EmailStr,
                       user: Annotated[UserModel, Depends(get_current_user)]
                       ) -> dict[str, str] | None:
    """Обновит email пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return await UserCrud.patch_email_user(new_email=new_email, old_email=user.email)


@router.patch('/update_password')
async def update_password(new_password: str,
                          user: Annotated[UserModel, Depends(get_current_user)]
                          ) -> dict[str, str] | None:
    """Обновит password пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return await UserCrud.patch_password(new_password=new_password, email=user.email)


@router.delete('/delete_score')
async def delete_score(user: Annotated[UserModel, Depends(get_current_user)]) -> dict[str, str] | None:
    """Удалит счет пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return await ScoreCrud.delete_score_user(user.email)
