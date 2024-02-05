from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    pass


class InvalidUserIDException(HTTPException):
    pass


class UserHasAccountException(Exception):
    pass


class InvalidEmailException(Exception):
    pass
