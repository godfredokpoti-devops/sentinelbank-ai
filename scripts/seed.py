import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
import json
from datetime import datetime
from pathlib import Path
from app.db.session import Base, SessionLocal, engine
from app.models.entities import Case, Customer, Transaction

Base.metadata.create_all(bind=engine)
data = json.loads(Path("data/synthetic/cases.json").read_text())
db = SessionLocal()
try:
    if db.query(Customer).count() == 0:
        db.add_all([Customer(**c) for c in data["customers"]])
        db.add_all([Case(**c) for c in data["cases"]])
        db.add_all([Transaction(**{**t, "occurred_at": datetime.fromisoformat(t["occurred_at"])}) for t in data["transactions"]])
        db.commit()
        print("Seeded synthetic banking data.")
    else:
        print("Database already contains seed data; no changes made.")
finally:
    db.close()
