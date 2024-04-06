# fastapi-example

## What is create_table.py for?

**app/core/database/create_table.py** is independent from this project.
It's for initializing MySQL Database.

## Setting ENVs

Before launching uvicorn server, set environment variables below.

- DB_HOST
- DB_PASSWORD
- DB_HOST
- DB_PORT
- DATABASE
- API_KEY

You can set envs with creating **app/.env** for python-dotenv or in Dockerfile.
These variables are refered from **Config** class in **app/config.py**.
