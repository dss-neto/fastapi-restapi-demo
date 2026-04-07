# RestAPI Task Manager

## Overview

This project implements a backend service where users can:

- Register and login using JWT authentication
- Create, read, update and delete their own tasks

## Features

- JWT authentication (needed to use the app)
- Password hashing using bcrypt
- User registration, login and deletion
- Task CRUD operations + checking
- Pagination support for task listing
- Users can only access their own tasks

## Tech-stack

- Python (backend programming language)
- FastAPI (backend)
- Pydantic (validation)
- SQLite (database)
- SQLAlchemy (ORM)
- JWT (authentication)
- bcrypt (password hashing)

## Goal

This project's goal was to learn databases and authentication.

## Installation

```bash
git clone https://github.com/dss-neto/fastapi-restapi-demo
cd <project>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Apllication:

```bash
uvicorn src.backend.main:app --reload
```

API will be available at:
http://127.0.0.1:8000

Interactive docs:
http://127.0.0.1:8000/docs

## License

RestAPI Task Manager is licensed under the [MIT License](https://opensource.org/licenses/MIT).
