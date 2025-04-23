from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class Base(BaseModel):
    pass


class UserModel(Base):
    """Валидация пользователя"""
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    state: bool
    role: str = 'basic'

    model_config = ConfigDict(from_attributes=True)


class PaymentModel(Base):
    """Валидация платежа"""
    transaction_id: int
    score_id: int
    user_id: int
    amount: Decimal
    signature: str


class AdminModel(UserModel):
    """Валидация админа"""
    role: str = 'admin'


class TokenModel(Base):
    """Валидация токена"""
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'

