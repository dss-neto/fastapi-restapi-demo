from re import match
from fastapi import HTTPException


def validate_email(email: str):
    pattern = r"^[A-Za-z0-9_.]+@[a-z]+\.[a-z]{2,4}$"
    if not match(pattern, email):
        raise HTTPException(
            status_code=422,
            detail="Invalid email",
        )


def validate_token(auth_header: str):
    if (
        auth_header == None
        or auth_header[:7] != "Bearer "
        or auth_header == "Bearer "
    ):
        raise_unauthorized_error()


def raise_unauthorized_error():
    raise HTTPException(
        status_code=401,
        detail="Unauthorized",
    )


def raise_forbidden_error():
    raise HTTPException(
        status_code=403,
        detail={"error": "Forbidden"},
    )


def raise_no_content():
    raise HTTPException(
        status_code=204,
    )
