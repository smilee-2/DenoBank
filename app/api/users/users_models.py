from fastapi import APIRouter, Depends

from app.api.models import UserModel
from app.core.database.schemas import UserSchemas
from app.core.database.crud import UserCrud


router = APIRouter(tags=['users'], prefix='/users')


@router.get('/get_user_by_id')
async def get_user(user_id: int):
    user = await UserCrud.get_user_by_id(user_id=user_id)
    return user if user else {'msg': 'user not found'}

