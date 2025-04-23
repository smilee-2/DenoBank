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
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[bool] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    score: Mapped[list["ScoreSchemas"]] = relationship(back_populates="user",cascade='all, delete-orphan',passive_deletes=True,)


class ScoreSchemas(Base):
    __tablename__ = "scores"

    score_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    score: Mapped[Decimal] = mapped_column(nullable=False, default=Decimal('0.0'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped["UserSchemas"] = relationship(
        back_populates="score",
    )


class PaymentSchemas(Base):
    __tablename__ = 'payments'

    payment_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    score_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    transaction_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(nullable=False)
    signature: Mapped[str] = mapped_column(nullable=False)
    datetime_payment: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
