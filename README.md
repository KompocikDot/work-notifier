# workifier

> Project monitoring few popular job-related websites **(like justjoin.it)** for new job advertisements. New ads are filtered and if they meet criteria they are sent to the user through discord webhook

### Dependencies and technologies used:
- requests
- discord_webhook
- pytest
- postgreSQL
- docker

### Formatting and typechecking
- black
- flake8
- isort
- mypy

## Requirements
1. PostgreSQL 14+
2. Python 3.10+
> OR
1. Docker
2. Docker compose

> **Optionally Make**

## Usage

1. Clone git repository using `git clone git@github.com:KompocikDot/workifier.git`
2. Rename `.db.example` to `.db` and `.notifier.example` to `.notifier` and fill the variables in both files
> Without Docker and Make
3. Run `python app/main.py` or `python3 app/main.py` for linux/macOS
> With Docker and Make
3. Run `make build && make run`


## NOTE: at the moment project is in POC phase

## Roadmap
- Add more sites
  - [pracuj.pl](https://it.pracuj.pl)
  - [bulldogjob](https://bulldogjob.pl)
  - [nofluffjobs](https://nofluffjobs.com/pl/)
- Write tests
- Add more filters eg. salary, employment type
- Cleanup code of both databases and notifier(make code more generic) 
- Add more options to notify(?)
  - Slack
  - SMS
  - Email
