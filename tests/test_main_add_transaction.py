from datetime import date

from sqlalchemy import select

from main import add_transaction
from models import Transaction


def _set_inputs(monkeypatch, values):
    iterator = iter(values)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(iterator))


def test_add_transaction_reprompts_on_non_positive_amount(session, wallet, monkeypatch, capsys):
    _set_inputs(
        monkeypatch,
        ["-10", "100", "expense", "food", "2026-01-05"],
    )

    add_transaction(session, wallet)
    output = capsys.readouterr().out

    assert "amount must be greater than 0" in output

    transactions = session.scalars(select(Transaction).where(Transaction.wallet_id == wallet.id)).all()
    assert len(transactions) == 1
    assert transactions[0].amount == 100.0
    assert transactions[0].transaction_date == date(2026, 1, 5)
    assert wallet.budget.spent == 100.0