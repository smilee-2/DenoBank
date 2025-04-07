from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class Base(DeclarativeBase):
    pass


class UserSchemas(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=True, nullable=False)
    state: Mapped[bool] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    score: Mapped[list["ScoreSchemas"]] = relationship(back_populates="user")


class ScoreSchemas(Base):
    __tablename__ = "scores"

    score_id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[Decimal] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped["UserSchemas"] = relationship(back_populates="score")


class PaymentSchemas(Base):
    __tablename__ = 'payments'

    payment_id: Mapped[int] = mapped_column(primary_key=True)
    datetime_payment: Mapped[datetime] = mapped_column(default=datetime.now)
    from_user: Mapped[str] = mapped_column(nullable=False)
    to_user: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[Decimal] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
