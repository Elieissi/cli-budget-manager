from datetime import date

from models import Budget, Transaction, Wallet


def test_get_balance_returns_zero_for_empty_wallet(session, wallet):
    assert wallet.get_balance(session) == 0.0


def test_get_balance_subtracts_expenses_from_income(session, wallet):
    session.add_all(
        [
            Transaction(
                amount=200.0,
                type="income",
                category="salary",
                transaction_date=date(2026, 1, 1),
                wallet_id=wallet.id,
            ),
            Transaction(
                amount=50.0,
                type="expense",
                category="food",
                transaction_date=date(2026, 1, 2),
                wallet_id=wallet.id,
            ),
            Transaction(
                amount=25.0,
                type="expense",
                category="transport",
                transaction_date=date(2026, 1, 3),
                wallet_id=wallet.id,
            ),
        ]
    )
    session.commit()

    assert wallet.get_balance(session) == 125.0


def test_get_balance_uses_only_wallet_transactions(session, wallet):
    other_wallet = Wallet(name="Other Wallet")
    other_wallet.budget = Budget(limit=500, spent=0)
    session.add(other_wallet)
    session.commit()
    session.refresh(other_wallet)

    session.add_all(
        [
            Transaction(
                amount=100.0,
                type="income",
                category="salary",
                transaction_date=date(2026, 1, 1),
                wallet_id=wallet.id,
            ),
            Transaction(
                amount=999.0,
                type="income",
                category="bonus",
                transaction_date=date(2026, 1, 1),
                wallet_id=other_wallet.id,
            ),
            Transaction(
                amount=999.0,
                type="expense",
                category="rent",
                transaction_date=date(2026, 1, 2),
                wallet_id=other_wallet.id,
            ),
        ]
    )
    session.commit()

    assert wallet.get_balance(session) == 100.0
