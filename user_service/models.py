from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class LogoutRequest(BaseModel):
    user_id: str