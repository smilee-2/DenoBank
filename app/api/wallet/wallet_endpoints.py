from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depends.depends import get_current_user, get_password_hash, verify_password
from app.api.models.models import PaymentModel, UserModel
from app.core.database.crud import ScoreCrud, PaymentCrud
from app.core.config.config import setting_check_sig, HTTP_BEARER

router = APIRouter(prefix='/wallets', tags=['Wallet'], dependencies=[Depends(HTTP_BEARER)])


@router.get('/get_user_scores')
async def get_user_scores(user: Annotated[UserModel, Depends(get_current_user)]) -> dict | None:
    """Получить счета пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return await ScoreCrud.get_user_scores(email=user.email)


@router.get('/create_new_score')
async def create_new_score(user: Annotated[UserModel, Depends(get_current_user)]) -> dict[str, str]:
    """Создаст новый счет пользователя"""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')
    return await ScoreCrud.create_new_score(email=user.email)


@router.post('/top_up_the_users_balance')
async def top_up_the_users_balance(payment: Annotated[PaymentModel, Depends()],
                                   user: Annotated[UserModel, Depends(get_current_user)]
                                   ) -> dict[str, str] | None:
    """Зачислит деньги на счет. Обрабатывает вебхук от сторонней платежной системы."""
    if not user.state:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user disable')

    concatenated_string = (f"{payment.score_id}{payment.amount}{payment.transaction_id}"
                           f"{payment.user_id}{setting_check_sig.SECRET_KEY}")
    expected_signature = get_password_hash(concatenated_string.encode())

    if verify_password(payment.signature, expected_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    return await PaymentCrud.transfer_money(amount=payment.amount,
                                            score_id=payment.score_id,
                                            user_id=payment.user_id,
                                            payment=payment)
