# fastapi-example

## What is create_table.py for?

**app/core/database/create_table.py** is independent from this project.
It's for initializing MySQL Database.

## Setting Environment Variables

Before launching uvicorn server, you must set environment variables below.

- DB_HOST
- DB_PASSWORD
- DB_HOST
- DB_PORT
- DATABASE
- API_KEY

These variables are refered from **Config** class in **app/config.py**.

You can set envs through creating **.env** in parent directory of **app**
for both python-dotenv and docker-compose.
If you open docker-compose.yml, you can see where the compose file read envs from.

Or, you can set envs in Dockerfile to configure envs while building docker image.
