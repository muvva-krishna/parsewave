backend-install:
	cd backend && python -m pip install -e '.[all]'

test:
	python -m pytest -q

api:
	cd backend && uvicorn app.main:app --reload --port 8000

infra:
	docker compose -f infra/docker-compose.yml up -d
