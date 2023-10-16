from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
