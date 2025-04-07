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
    role: str

    model_config = ConfigDict(from_attributes=True)


class TokenModel(Base):
    """Валидация токена"""
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'



class TokenData(Base):
    username: str | None = None