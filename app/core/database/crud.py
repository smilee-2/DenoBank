from decimal import Decimal

from pydantic import EmailStr
from sqlalchemy import select

from app.api.models import UserModel
from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, ScoreSchemas, PaymentSchemas


class UserCrud:

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserModel | None:
        """Вернет пользователя по id"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            if user:
                return UserModel.model_validate(user)

    @staticmethod
    async def get_user_id(email: EmailStr) -> int | None:
        """Вернет id пользователя"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user.id

    @staticmethod
    async def get_user_email(user_id: int) -> int | None:
        """Вернет email пользователя"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            if user:
                return user.email

    @staticmethod
    async def get_user_by_email(email: str) -> UserModel | None:
        """Вернет пользователя по email"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(user)

    @staticmethod
    async def create_user(user_input: UserModel) -> dict[str, str]:
        """Создаст пользователя"""
        async with session_maker.begin() as session:
            user = UserSchemas(**user_input.model_dump())
            session.add(user)
            await session.flush()

            score = ScoreSchemas(score=Decimal('0.0'), user_id=user.id)
            session.add(score)
            return {'message': 'user was created'}

    @staticmethod
    async def update_user(user_id: int, new_user: UserModel) -> dict[str, str] | None:
        """Полностью обновит пользователя"""
        async with session_maker.begin() as session:
            stmt = select(UserSchemas).where(
                UserSchemas.id == user_id
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user = UserSchemas(**new_user.model_dump())
                return {'msg': 'user was update'}

    @staticmethod
    async def patch_email_user_for_admin(new_email: EmailStr, old_email: EmailStr) -> dict[str, str] | None:
        """Обновит email пользователя"""
        async with session_maker.begin() as session:
            stmt = select(UserSchemas).where(
                UserSchemas.email == old_email
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.email = new_email
                return {'msg': 'email was update'}

    @staticmethod
    async def patch_email_user(new_email: EmailStr, old_email: EmailStr) -> dict[str, str] | None:
        """Обновит email пользователя"""
        async with session_maker.begin() as session:
            stmt = select(UserSchemas).where(
                UserSchemas.email == old_email
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.email = new_email
                return {'msg': 'email was update'}

    @staticmethod
    async def patch_password(new_password: str, email: EmailStr) -> dict[str, str] | None:
        async with session_maker.begin() as session:
            stmt = select(UserSchemas).where(
                UserSchemas.email == email
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.password = new_password
                return {'msg': 'password was update'}

    @staticmethod
    async def delete_user_by_id(user_id: int) -> bool:
        """Удалит пользователя из БД по id"""
        async with session_maker.begin() as session:
            await session.delete(UserSchemas, user_id)
            return True


class ScoreCrud:

    @staticmethod
    async def get_user_score(email: EmailStr) -> Decimal | None:
        """Получить счет пользователя"""
        async with session_maker.begin() as session:
            user_id = await UserCrud.get_user_id(email)
            query = select(ScoreSchemas).where(ScoreSchemas.user_id == user_id)
            result = await session.execute(query)
            score = result.scalar_one_or_none()
            if score:
                return score.score


class PaymentCrud:
    @staticmethod
    async def transfer_money(amount: Decimal):
        """Зачислить деньги на счет"""
        async with session_maker.begin() as session:
            query = select()
            ...

    @staticmethod
    async def withdraw_money(amount: Decimal):
        """Снять деньги со счета"""
        async with session_maker.begin() as session:
            ...
