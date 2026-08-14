install:
	python -m pip install -r requirements.txt
seed:
	python scripts/seed.py
run:
	uvicorn app.main:app --reload
test:
	pytest -q
lint:
	ruff check .
evaluate:
	python scripts/evaluate.py
docker:
	docker compose up --build
