from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    validator,
    root_validator,
)
from .models import User


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


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
