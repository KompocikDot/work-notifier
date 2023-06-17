build:
	docker-compose build

run:
	docker-compose up

test:
	pytest

pc:
	pre-commit run -a
