import bcrypt
from src.backend.tertiary.json_web_tokens import generate_user_token
from src.backend.tertiary.formatter import format_user_list
from src.backend.tertiary.validation import (
    validate_email,
    raise_no_content,
    raise_forbidden_error,
)
from src.backend.database.models import User, Task
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from src.backend.main import UserSchema


def operation_register_user(
    user: UserSchema,
    session: Session
):
    validate_email(user.email)

    # encode to bytes (the result isn't a string, but a object of the bytes class)
    password_bytes = user.password.encode("utf-8")

    # hashing the password in bytes and the salt
    # the result is again a object (instance) of bytes, not a string
    hashed = bcrypt.hashpw(password=password_bytes, salt=bcrypt.gensalt())

    # turns the (password_bytes + salt) hashes back into a string
    hashed_string = hashed.decode("utf-8")
    # Temporary
    if user.role == "Admin":
        role = "Admin"
    elif user.role == "Owner":
        role = "Owner"
    else: role = "Basic"
        
    user_registered = User(
        name=user.name,
        role=role,
        email=user.email,
        hashed_password=hashed_string,
    )
    
    session.add(user_registered)
    session.commit()
    session.refresh(user_registered)
    token = generate_user_token(user_registered.id, user.email, user.role)

    return {
        "message": "You've sucessfuly registered.",
        "User": {
            "userId": user_registered.id,
            "name": user_registered.name,
            "email": user_registered.email,
            "role": user_registered.role
        },
        "Token": token,
    }


def operation_login_user(
    user: UserSchema,
    session: Session
):
    validate_email(user.email)
    # stmt= select(
        # User.name, User.hashed_password, User.id
        # ).where(User.email == user.email)
    stmt = select(User).where(User.email == user.email)
    user_data = session.execute(stmt).scalars().first()

    # encodes both the password given and the password stored to bytes object
    password_bytes = user.password.encode("utf-8")
    stored_hash_bytes = user_data.hashed_password.encode("utf-8")

    # compares the encoded passwords
    if bcrypt.checkpw(password_bytes, stored_hash_bytes):
        token = generate_user_token(user_data.id, user.email, user_data.role)
        return {
            "message": f"Welcome {user_data.name}! You've successfully logged in.",
            "Token": token,
        }
    else:
        return {"error": "Incorrect email or password. Try again."}


def operation_read_user_list(
    session: Session
):
    stmt = select(User)
    user_list = session.execute(stmt).scalars().all()

    formatted_user_list = format_user_list(user_list)
    return formatted_user_list


def operation_delete_user(
    decoded_token_data: dict,
    user_id: int,
    session: Session
):
    if decoded_token_data["role"] == "Owner":
        stmt = delete(Task).where(Task.owner_user_id == user_id)
        session.execute(stmt)
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
        raise_no_content()
        
        
    elif decoded_token_data["role"] == "Admin":
        stmt = select(User.role).where(User.id == user_id)
        target_role = session.execute(stmt).scalars().first()
        if target_role == "Basic" or not target_role:
            stmt = delete(Task).where(Task.owner_user_id == user_id)
            session.execute(stmt)
            stmt = delete(User).where(User.id == user_id)
            session.execute(stmt)
            session.commit()
            raise_no_content()
    
    
    elif user_id == int(decoded_token_data["sub"]):
        stmt = delete(Task).where(Task.owner_user_id == user_id)
        session.execute(stmt)
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
        raise_no_content()
        
    raise_forbidden_error()