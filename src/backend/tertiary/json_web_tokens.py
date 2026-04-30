import jwt
from src.backend.tertiary.validation import (
    validate_token,
    raise_unauthorized_error,
)
from dotenv import load_dotenv
from os import getenv

load_dotenv()
SECRET_KEY = getenv("secret_key")


def generate_user_token(user_id: int, user_email: str):
    payload_data = {"sub": str(user_id), "email": user_email}
    token = jwt.encode(
        payload=payload_data,
        key=SECRET_KEY,
    )

    return token


def decode_jwt_token(token):
    decoded = jwt.decode(token, SECRET_KEY, ["HS256"])
    return decoded


def get_decoded_token(request: object):
    auth_header = request.headers.get("Authorization")  # "Bearer {token}"
    validate_token(auth_header)
    jwt_token = auth_header.split()[1]  # ["Bearer", "{token}"]
    try:
        decoded_token_data = decode_jwt_token(jwt_token)
    except jwt.exceptions.DecodeError:
        raise_unauthorized_error()
    return decoded_token_data
