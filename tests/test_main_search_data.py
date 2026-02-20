from datetime import date

from main import search_data
from models import Transaction


def _set_inputs(monkeypatch, values):
    iterator = iter(values)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(iterator))


def _seed_transactions(session, wallet):
    session.add_all(
        [
            Transaction(
                amount=100.0,
                type="income",
                category="salary",
                transaction_date=date(2026, 1, 2),
                wallet_id=wallet.id,
            ),
            Transaction(
                amount=25.0,
                type="expense",
                category="food",
                transaction_date=date(2026, 1, 1),
                wallet_id=wallet.id,
            ),
            Transaction(
                amount=40.0,
                type="expense",
                category="transport",
                transaction_date=date(2026, 1, 3),
                wallet_id=wallet.id,
            ),
        ]
    )
    session.commit()


def test_search_data_type_filter_expense_shows_only_expense_rows(session, wallet, monkeypatch, capsys):
    _seed_transactions(session, wallet)
    _set_inputs(monkeypatch, ["2", "1"])

    search_data(wallet, session)
    output = capsys.readouterr().out

    assert "Amount   Type       Category    Date" in output
    assert "expense" in output
    assert "income" not in output
    assert "food" in output
    assert "transport" in output


def test_search_data_type_filter_income_shows_only_income_rows(session, wallet, monkeypatch, capsys):
    _seed_transactions(session, wallet)
    _set_inputs(monkeypatch, ["2", "2"])

    search_data(wallet, session)
    output = capsys.readouterr().out

    assert "Amount   Type       Category    Date" in output
    assert "income" in output
    assert "salary" in output
    assert "expense" not in output


def test_search_data_date_range_inclusive_between(session, wallet, monkeypatch, capsys):
    _seed_transactions(session, wallet)
    _set_inputs(monkeypatch, ["1", "2026-01-01", "2026-01-02"])

    search_data(wallet, session)
    output = capsys.readouterr().out

    assert "2026-01-01" in output
    assert "2026-01-02" in output
    assert "2026-01-03" not in output
    assert output.find("2026-01-01") < output.find("2026-01-02")


def test_search_data_empty_result_prints_no_transactions_found(session, wallet, monkeypatch, capsys):
    _set_inputs(monkeypatch, ["2", "1"])

    search_data(wallet, session)
    output = capsys.readouterr().out

    assert "No transactions found." in output
