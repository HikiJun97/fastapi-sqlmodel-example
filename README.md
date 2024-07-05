# fastapi-sqlmodel-example

This is a simple async example of FastAPI with SQLModel. There's no async code in SQLModel documentation yet, so I decided to create this example.

## Issue of sqlmodel.Field

There is an issue with the sqlmodel.FieldInfo class, which inherits from the pydantic.FieldInfo class. Starting from Pydantic v2, it uses the argument "pattern" instead of "regex", but SQLModel still only accepts "regex". By adding the "pattern" argument to the Field module, which creates a FieldInfo instance, you can use the "pattern" argument in sqlmodel.Field in the same way as in pydantic.Field.

## Setting Environment Variables

If you want to use your own database, you need to change the environment variables in the docker-compose.yml file.

- DB_HOST
- DB_PASS
- DB_HOST
- DB_PORT
- DB_NAME
- API_KEY

These variables are refered from **Config** class in **app/config.py**.
