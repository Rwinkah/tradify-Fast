from pydantic import BaseModel, EmailStr
from ...user.schema import UserCreate


class AuthLogin(BaseModel):
    email: EmailStr
    password: str



class AuthRegister(UserCreate):
    pass


class AuthVerifyEmail(BaseModel):
    email: EmailStr
    otp: str