from datetime import timedelta

from fastapi import APIRouter, Response, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.main import get_db
from models.database import User
from models.user import RegisterRequest, UserInfo, Token
from utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user

user_router = APIRouter(prefix="/user")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_router.post("/register")
async def user_register(body: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    try:
        db.add(User(usr=body.username, email=body.email, pwd=pwd_context.hash(body.password)))
        db.commit()
        return Response(status_code=201)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")


@user_router.post("/login")
async def user_login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # noinspection PyTypeChecker
    user = db.query(User).filter(User.email == body.username).first()
    if user is not None and pwd_context.verify(body.password, user.pwd):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})


@user_router.get("/me")
async def user_info(current_user: User = Depends(get_current_user)):
    return UserInfo(id=current_user.id, username=current_user.usr, email=current_user.email)
