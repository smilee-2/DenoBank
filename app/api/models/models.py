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


class Payment(Base):
    transaction_id: str
    account_id: int
    user_id: int
    amount: Decimal
    signature: str


class AdminModel(UserModel):
    """Валидация админа"""
    role: str = 'admin'


class TokenModel(Base):
    """Валидация токена"""
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'



class TokenData(Base):
    username: str | None = None