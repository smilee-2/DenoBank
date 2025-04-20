from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.depends.depends import get_current_user
from app.api.models.models import Payment, UserModel
from app.core.database.crud import ScoreCrud, PaymentCrud

router = APIRouter(prefix='/wallets', tags=['Wallet'])

@router.get('/get_user_score')
async def get_user_score(user: Annotated[UserModel, Depends(get_current_user)]):
    return await ScoreCrud.get_user_score(user.email)

@router.post('/top_up_the_users_balance')
async def top_up_the_users_balance(payment: Annotated[Payment, Depends()], user: Annotated[UserModel, Depends(get_current_user)]):
    result = await PaymentCrud.transfer_money(payment.amount)