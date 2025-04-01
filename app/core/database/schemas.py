from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DECIMAL = Numeric(precision=10)

class Base(DeclarativeBase):
    pass


class UserSchemas(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    score: Mapped[list["ScoreSchemas"]] = relationship(back_populates="user")


class ScoreSchemas(Base):
    __tablename__ = "scores"

    score: Mapped[DECIMAL] = mapped_column(nullable=False)
    user: Mapped["UserSchemas"] = relationship(back_populates="score")

