from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    validator,
    root_validator,
)
from . import auth
from .models import User


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
    session_id: str = None

    @root_validator(pre=True, skip_on_failure=True)
    def validate_user(cls, values):
        err_msg = "Incorrect credentials, please try again."
        email = values.get("email") or None
        password = values.get("password") or None
        if email is None or password is None:
            raise ValueError(err_msg)
        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(err_msg)
        token = auth.login(user_obj)
        return {"session_id": token}


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    @validator('email')
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError('Email is not available')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        password = values.get('password')
        confirm_password = v
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return v
