# TODO: ADD TESTING WITH PYTEST
# TODO: ROLES:
#             ADMINS CAN DELETE AND READ USER DB
#             GENERAL USERS CAN ONLY CREATE AND DELETE THEIR OWN ROW IN USER DB
# TODO: SIMPLE FRONT END

from fastapi import FastAPI, Request

# APIs is the mean of communication between client and server/backend
# it acts like a restaurant waiter, where the client is the customer and the server is the kitchen
from fastapi.params import Body
from pydantic import BaseModel

# BaseModel makes it so fastapi automatically validates, parses and request from body
from operations.user_operations import (
    operation_register_user,
    operation_read_user_list,
    operation_login_user,
    operation_delete_user,
)
from operations.task_operations import (
    operation_create_task,
    operation_get_task_list,
    operation_get_single_task,
    operation_update_task,
    operation_delete_task,
)
from tertiary.json_web_tokens import (
    get_decoded_token,
)

app = FastAPI()

# = = = = USERS = = = =


class UserSchema(BaseModel):
    name: str  # because of BaseModel, FastApi will check if the sent data is really a string
    email: str  # unique
    password: str
    # basemodel also makes pydantic parse data
    # example: {"name": "Bob"} -> "Bob"
    # pasing: convert raw data to usable data


@app.post("/register")
# /register is the route
def register_user(user: UserSchema = Body(...)):

    # http method + route + function = endpoint
    return operation_register_user(user)


@app.get("/")
def read_user_list():
    return operation_read_user_list()


@app.post("/login")
def login_user(user: UserSchema = Body(...)):
    return operation_login_user(user)


@app.delete("/{user_id}")
def delete_user(request: Request, user_id: int):
    decoded_token_data = get_decoded_token(request)
    return operation_delete_user(decoded_token_data, user_id)


# = = = = TASKS = = = =


class TaskSchema(BaseModel):
    title: str
    description: str
    is_checked: int


@app.post("/tasks")
def create_task(request: Request, task: TaskSchema = Body(...)):
    decoded_token_data = get_decoded_token(request)
    return operation_create_task(task, decoded_token_data)


@app.get("/tasks")
def read_task_list(
    request: Request, page: int | None = None, limit: int | None = None
):
    decoded_token_data = get_decoded_token(request)
    return operation_get_task_list(decoded_token_data, page, limit)


@app.get("/tasks/{task_id}")
def read_task(request: Request, task_id: int):
    decoded_token_data = get_decoded_token(request)
    return operation_get_single_task(task_id, decoded_token_data)


@app.put("/tasks/{task_id}")
def update_task(request: Request, task_id: int, task: TaskSchema = Body(...)):
    decoded_token_data = get_decoded_token(request)
    return operation_update_task(task_id, task, decoded_token_data)


@app.delete("/tasks/{task_id}")
def delete_task(request: Request, task_id: int):
    decoded_token_data = get_decoded_token(request)
    return operation_delete_task(task_id, decoded_token_data)
