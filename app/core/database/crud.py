from decimal import Decimal

from pydantic import EmailStr
from sqlalchemy import select

from app.api.models import UserModel, PaymentModel, PaymentDateModel
from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, ScoreSchemas, PaymentSchemas


class UserCrud:

    @staticmethod
    async def get_all_users() -> list[UserModel]:
        """Вернет всех пользователей"""
        async with session_maker.begin() as session:
            query = select(UserSchemas)
            result = await session.execute(query)
            users = result.scalars().all()
            print(users)
            return [UserModel.model_validate(user) for user in users]

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserModel | dict[str, str]:
        """Вернет пользователя по id"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            if user:
                return UserModel.model_validate(user)
            return {'msg': 'user not found'}

    @staticmethod
    async def get_user_id(email: EmailStr) -> int | dict[str, str]:
        """Вернет id пользователя"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user.id
            return {'msg': 'user not found'}

    @staticmethod
    async def get_user_email(user_id: int) -> int | dict[str, str]:
        """Вернет email пользователя"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            if user:
                return user.email
            return {'msg': 'user not found'}

    @staticmethod
    async def get_user_by_email(email: str) -> UserModel | dict[str, str]:
        """Вернет пользователя по email"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(user)
            return {'msg': 'user not found'}

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
    async def update_user(user_id: int, new_user: UserModel) -> dict[str, str]:
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
            return {'msg': 'user not found'}

    @staticmethod
    async def patch_email_user_for_admin(new_email: EmailStr, old_email: EmailStr) -> dict[str, str]:
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
            return {'msg': 'user not found'}

    @staticmethod
    async def patch_email_user(new_email: EmailStr, old_email: EmailStr) -> dict[str, str]:
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
            return {'msg': 'user not found'}

    @staticmethod
    async def patch_password(new_password: str, email: EmailStr) -> dict[str, str]:
        """Обновит password пользователя"""
        async with session_maker.begin() as session:
            stmt = select(UserSchemas).where(
                UserSchemas.email == email
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.password = new_password
                return {'msg': 'password was update'}
            return {'msg': 'user not found'}

    @staticmethod
    async def delete_user_by_id(user_id: int) -> dict[str, str]:
        """Удалит пользователя из БД по id"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)

            await session.delete(user)
            return {'msg': 'user was deleted'}

    @staticmethod
    async def disable_user(email: EmailStr) -> dict[str, str]:
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                user.state = False
                return {'message': 'user was disabled'}
            return {'msg': 'user not found'}

    @staticmethod
    async def enable_user(email: EmailStr) -> dict[str, str]:
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                user.state = True
                return {'message': 'user was enabled'}
            return {'msg': 'user not found'}


class ScoreCrud:

    @staticmethod
    async def get_user_scores(email: EmailStr) -> dict:
        """Получить счета пользователя"""
        async with session_maker.begin() as session:
            user_id = await UserCrud.get_user_id(email=email)
            query = select(ScoreSchemas).where(ScoreSchemas.user_id == user_id)
            result = await session.execute(query)
            scores = result.scalars()
            if scores:
                return {idx: score.score for idx, score in enumerate(scores)}
            return {'msg': 'scores not found'}

    @staticmethod
    async def create_new_score(email: EmailStr) -> dict[str, str]:
        """Создаст новый счет пользователя"""
        async with session_maker.begin() as session:
            user_id = await UserCrud.get_user_id(email=email)
            score = ScoreSchemas(score=Decimal('0.0'), user_id=user_id)
            session.add(score)
            return {'msg': 'score was created'}

    @staticmethod
    async def delete_score_user(email: EmailStr) -> dict[str, str]:
        """Удалит счет пользователя"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.email == email).subquery()
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                await session.delete(ScoreSchemas, user.id)
                await session.delete(PaymentSchemas, user.id)
                return {'msg': 'score was deleted'}
            return {'msg': 'score not found'}


class PaymentCrud:
    @staticmethod
    async def transfer_money(amount: Decimal,
                             user_id: int,
                             score_id: int,
                             payment: PaymentModel
                             ) -> dict[str, str]:
        """Зачислить деньги на счет"""
        async with session_maker.begin() as session:
            query = select(ScoreSchemas).filter_by(score_id=score_id, user_id=user_id)
            result_for_score = await session.execute(query)
            score = result_for_score.scalar_one_or_none()
            if score:
                score.score += amount
                pay = PaymentSchemas(**payment.model_dump())
                session.add(pay)
                return {'msg': 'the money is credited'}
            return {'msg': 'score not found'}

    @staticmethod
    async def get_all_payments(user_id: int) -> list[PaymentModel]:
        """Вернет платежи пользователя"""
        async with session_maker.begin() as session:
            query = select(PaymentSchemas).where(PaymentSchemas.user_id == user_id)
            result = await session.execute(query)
            payments = result.scalars().all()
            return [PaymentDateModel.model_validate(payment) for payment in payments]

