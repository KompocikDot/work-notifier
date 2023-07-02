build:
	docker-compose build

run:
	docker-compose up

test:
	python -m unittest

pc:
	pre-commit run -a
