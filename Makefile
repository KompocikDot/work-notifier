build:
	docker-compose build

run:
	docker-compose up

test:
	pytest

pc:
	pre-commit autoupdate
	pre-commit run -a
