from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models import Budget, Wallet


def _build_session_factory():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return engine, factory


import pytest


@pytest.fixture
def engine():
    engine, _ = _build_session_factory()
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def session(engine):
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    with factory() as session:
        yield session


@pytest.fixture
def wallet(session):
    wallet = Wallet(name="Test Wallet")
    wallet.budget = Budget(limit=1000, spent=0)
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet
