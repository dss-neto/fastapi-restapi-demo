# TODO: JWT expires after 60 minutes
# TODO: SIMPLE FRONT END

from jwt.exceptions import ExpiredSignatureError
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from src.backend.database.db import engine
from src.backend.tertiary.validation import raise_unauthorized_error

# APIs is the mean of communication between client and server/backend
# it acts like a restaurant waiter, where the client is the customer and the server is the kitchen
from fastapi.params import Body
from pydantic import BaseModel
# BaseModel makes it so fastapi automatically validates, parses and request from body


app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

# = = = = USERS = = = =


class UserSchema(BaseModel):
    name: str  # because of BaseModel, FastApi will check if the sent data is really a string
    email: str  # unique
    password: str
    # basemodel also makes pydantic parse data
    # example: {"name": "Bob"} -> "Bob"
    # parsing: convert raw data to usable data
    
    # Temporary:
    role: str
    
class UserLoginSchema(BaseModel):
    email: str
    password: str



@app.post("/register")
# /register is the route
def register_user(
    user: UserSchema = Body(...),
    session: Session = Depends(get_session)    
):
    from src.backend.operations.user_operations import operation_register_user

    # http method + route + function = endpoint
    return operation_register_user(user, session)


@app.get("/")
def read_user_list(
    request: Request,
    session: Session = Depends(get_session)
):
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    from src.backend.operations.user_operations import operation_read_user_list
    from src.backend.tertiary.validation import raise_forbidden_error
    
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
    if decoded_token_data["role"] == "Basic":
        raise_forbidden_error()
    
    return operation_read_user_list(session)


@app.post("/login")
def login_user(
    user: UserLoginSchema = Body(...),
    session: Session = Depends(get_session)
):
    from src.backend.operations.user_operations import operation_login_user
    # {email, password}
    
    return operation_login_user(user, session)


@app.delete("/{user_id}")
def delete_user(
    request: Request,
    user_id: int,
    session: Session = Depends(get_session)
):
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    from src.backend.operations.user_operations import operation_delete_user
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
        
    return operation_delete_user(decoded_token_data, user_id, session)


# = = = = TASKS = = = =


class TaskSchema(BaseModel):
    title: str
    description: str
    is_checked: int


@app.post("/tasks")
def create_task(
    request: Request,
    task: TaskSchema = Body(...),
    session: Session = Depends(get_session)
):
    from src.backend.operations.task_operations import operation_create_task
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
        
    return operation_create_task(task, decoded_token_data, session)


@app.get("/tasks")
def read_task_list(
    request: Request,
    page: int | None = None,
    limit: int | None = None,
    session: Session = Depends(get_session)
):
    from src.backend.operations.task_operations import operation_get_task_list
    from src.backend.tertiary.json_web_tokens import get_decoded_token
 
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
    
    return operation_get_task_list(decoded_token_data, page, limit, session)


@app.get("/tasks/{task_id}")
def read_task(
    request: Request, 
    task_id: int,
    session: Session = Depends(get_session)
):
    from src.backend.operations.task_operations import operation_get_single_task
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
        
    return operation_get_single_task(task_id, decoded_token_data, session)


@app.put("/tasks/{task_id}")
def update_task(
    request: Request,
    task_id: int,
    task: TaskSchema = Body(...),
    session: Session = Depends(get_session)
):
    from src.backend.operations.task_operations import operation_update_task
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
    
    return operation_update_task(task_id, task, decoded_token_data, session)


@app.delete("/tasks/{task_id}")
def delete_task(
    request: Request, 
    task_id: int,
    session: Session = Depends(get_session),
):
    from src.backend.operations.task_operations import operation_delete_task
    from src.backend.tertiary.json_web_tokens import get_decoded_token
    
    try:
        decoded_token_data = get_decoded_token(request)
    except ExpiredSignatureError:
        raise_unauthorized_error()
        
    return operation_delete_task(task_id, decoded_token_data, session)
