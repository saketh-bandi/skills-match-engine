install:
	pip install -r requirements.txt

run:
	uvicorn backend.app:app --reload

test:
	pytest -q
