# workifier

> Project monitoring few popular job-related websites **(like justjoin.it)** for new job advertisements. New ads are filtered and if they meet criteria they are sent to the user through discord webhook

### Dependencies and technologies used:
- `requests`
- `discord_webhook`
- `pytest`
- `postgreSQL`
- `docker`

### Formatting and typechecking
> Project is formatted using:
- black
- flake8
- isort
- mypy

## Usage

1. Clone git repository using `git clone git@github.com:KompocikDot/workifier.git`
2. Rename `.db.example` to `.db` and `.notifier.example` to `.notifier` and fill the variables in both files
> Without Docker and Make
3. Run `python main.py` or `python3 main.py` for linux/MacOS
> With Docker and Make
3. Run `make build && make run`


## NOTE: at the moment project is in POC phase
