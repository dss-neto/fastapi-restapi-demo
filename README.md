# RestAPI Task Manager

## Overview

A backend service where users can authenticate and manage their tasks.

## Technologies used

- Python (backend programming language)
- FastAPI (backend)
- Pydantic (validation)
- SQLite (database)
- SQLAlchemy (ORM)
- JWT (authentication and authorization)
- bcrypt (password hashing)

## Installation

```bash
git clone https://github.com/dss-neto/fastapi-restapi-demo
cd <project>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the app

```bash
uvicorn src.backend.main:app --reload
```

API will be available at:
http://127.0.0.1:8000

Interactive docs:
http://127.0.0.1:8000/docs

## License

RestAPI Task Manager is licensed under the [MIT License](https://opensource.org/licenses/MIT).
