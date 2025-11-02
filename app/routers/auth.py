from typing import Annotated
from fastapi import HTTPException, status, Response, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.utils.hashing import verify_password_func
from app.session_settup import session
from app.models import User
from app.schemas import UserLogin, Token
from app.utils.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_201_CREATED)
def create_user(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    result = select(User).where(User.email == user_credentials.username)
    user = session.scalars(result).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify_password_func(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # CREATE A TOKEN
    access_token = create_access_token(data= {"user_id": user.id})
    # RETURN TOKEN
    return Token(access_token=access_token, token_type= "bearer")