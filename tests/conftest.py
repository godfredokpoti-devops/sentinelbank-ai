import os
os.environ["DATABASE_URL"] = "sqlite:///./test_sentinelbank.db"
os.environ["API_KEY"] = "test-key"

import pytest
from fastapi.testclient import TestClient
from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.entities import Case, Customer, Transaction
from datetime import datetime


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(Customer(customer_ref="CUST-T1", full_name="Test Customer", country="US", risk_rating="MEDIUM", pep=False))
    db.add(Case(case_ref="CASE-T1", customer_ref="CUST-T1", status="OPEN"))
    for i, (amt, country) in enumerate([(12000,"GB"),(9000,"DE"),(15000,"AE")], start=1):
        db.add(Transaction(tx_ref=f"TX-T{i}", customer_ref="CUST-T1", amount=amt, currency="USD",
                           beneficiary=f"Beneficiary {i}", beneficiary_country=country,
                           is_new_beneficiary=True, occurred_at=datetime(2026,8,i)))
    db.commit(); db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app, headers={"X-API-Key": "test-key", "X-Analyst": "pytest.analyst"})
