from database.db import get_connection
import bcrypt
from tertiary.json_web_tokens import generate_user_token
from tertiary.formatter import format_user_list
from tertiary.validation import (
    validate_email,
    raise_no_content,
    raise_forbidden_error,
)


def operation_register_user(user: object):
    validate_email(user.email)
    connection = get_connection()
    cursor = connection.cursor()

    # encode to bytes (the result isn't a string, but a object of the bytes class)
    password_bytes = user.password.encode("utf-8")

    # hashing the password in bytes and the salt
    # the result is again a object (instance) of bytes, not a string
    hashed = bcrypt.hashpw(password=password_bytes, salt=bcrypt.gensalt())

    # turns the (password_bytes + salt) hashes back into a string
    hashed_string = hashed.decode("utf-8")

    cursor.execute(
        """
            INSERT INTO user_database
            (name, email, hashed_password)
            VALUES (?, ?, ?)
        """,
        (user.name, user.email, hashed_string),
    )
    connection.commit()

    cursor.execute(
        """
        SELECT id FROM user_database
        WHERE email = (?)
        """,
        (user.email,),
    )
    user_id = cursor.fetchall()[0][0]
    connection.close()

    token = generate_user_token(user_id, user.email)

    return {
        "message": "You've sucessfuly registered.",
        "User": user,
        "Token": token,
    }


def operation_login_user(user: object):
    validate_email(user.email)
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, hashed_password, id FROM user_database WHERE email = ?",
        (user.email,),
    )
    user_data = cursor.fetchall()
    connection.close()
    name, stored_hash_string, user_id = user_data[0]

    # encodes both the password given and the password stored to bytes object
    password_bytes = user.password.encode("utf-8")
    stored_hash_bytes = stored_hash_string.encode("utf-8")

    # compares the encoded passwords
    if bcrypt.checkpw(password_bytes, stored_hash_bytes):
        token = generate_user_token(user_id, user.email)
        return {
            "message": f"Welcome {name}! You've successfully logged in.",
            "Token": token,
        }
    else:
        return {"error": "Incorrect email or password. Try again."}


def operation_read_user_list():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user_database")
    user_list = cursor.fetchall()
    connection.close()
    formatted_user_list = format_user_list(user_list)
    return formatted_user_list


def operation_delete_user(
    decoded_token_data: dict,
    user_id: int,
):
    connection = get_connection()
    cursor = connection.cursor()
    if user_id == int(decoded_token_data["sub"]):
        cursor.execute(
            """
                DELETE FROM task_list
                WHERE owner_user_id = ?
            """,
            (user_id,),
        )
        cursor.execute(
            """
                DELETE FROM user_database 
                WHERE id = ?
            """,
            (user_id,),
        )
        connection.commit()
        connection.close()
        raise_no_content()
    connection.close()
    raise_forbidden_error()
