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

## Envs explanations(app settings)
- `KEYWRODS` - string - list of words to search in advert(delimited by comma)
- `CITY` - string - city to filter
- `REMOTE` - bool - true/false
- `MIN_SALARY` - int - only positive value
- `EXPERIENCE` - enum - intern/trainee/junior/mid/senior/lead
- `SKIP_NO_SALARY` - bool - true/false
- `REFRESH_RATE` - int - seconds to wait until next try to fetch data
- `SKIP_FILTERS` - bool - true/false
- `USE_PROXIES` - bool - true/false
- `DISCORD_WEBHOOK` - string - discord webhook url to post ads
## NOTE: at the moment project is in POC phase

## Roadmap
- Write tests
- Add more filters eg. salary, employment type 
- Add more options to notify(?)
  - Slack
  - SMS
  - Email


## Contributing
> If you want to contribute in this project, please open pull request OR write ideas directly to me.
