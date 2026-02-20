from datetime import date

from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Wallet(Base):
    """Stores transactions and one budget for a user wallet."""

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="Default Wallet")

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="wallet",
        cascade="all, delete-orphan",
        order_by="Transaction.transaction_date",
    )
    budget: Mapped["Budget"] = relationship(
        back_populates="wallet",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def get_balance(self, session) -> float:
        income_stmt = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.wallet_id == self.id,
            Transaction.type == "income",
        )
        expense_stmt = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.wallet_id == self.id,
            Transaction.type == "expense",
        )
        income_total = session.scalar(income_stmt)
        expense_total = session.scalar(expense_stmt)
        return float(income_total - expense_total)


class Budget(Base):
    """Tracks budget limit and spending for one wallet."""

    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit: Mapped[float] = mapped_column(Float, default=0)
    spent: Mapped[float] = mapped_column(Float, default=0)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), unique=True)

    wallet: Mapped[Wallet] = relationship(back_populates="budget")

    def record_expense(self, amount: float) -> None:
        self.spent += amount

    def is_exceeded(self) -> bool:
        return self.spent >= self.limit


class Transaction(Base):
    """Stores one financial transaction belonging to a wallet."""

    __tablename__ = "transactions"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)

    wallet: Mapped[Wallet] = relationship(back_populates="transactions")

    def __str__(self) -> str:
        return f"{self.amount}, {self.type}, {self.category}, {self.transaction_date.isoformat()}"