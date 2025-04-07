from sqlalchemy import select
from pydantic import EmailStr

from app.api.models import UserModel
from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, ScoreSchemas



class UserCrud:

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserModel | None:
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            return UserModel.model_validate(user)

    @staticmethod
    async def get_user_by_username(username: str) -> UserModel | None:
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.first_name == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(**user)

    @staticmethod
    async def get_user_by_email(email: EmailStr) -> UserModel | None:
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(**user)

    @staticmethod
    async def create_user(user_input: UserModel) -> dict[str, str]:
        async with session_maker.begin() as session:
            user = UserSchemas(**user_input.model_dump())
            session.add(user)
            return {'message': 'user was created'}

    @staticmethod
    async def delete_user_by_id(user_id: int) -> bool:
        async with session_maker.begin() as session:
            await session.delete(UserSchemas, user_id)
            return True