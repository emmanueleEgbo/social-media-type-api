from typing import Annotated
from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.utils.hashing import verify_password_func
from app.database import get_db
from app.models import User
from app.schemas import Token
from app.utils.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_201_CREATED)
def create_user(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    # Validate input
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Invalid Credentials")
    
    # Look up user
    result = select(User).where(User.email == user_credentials.username)
    user = db.scalars(result).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Verify password  
    if not verify_password_func(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # CREATE A TOKEN
    access_token = create_access_token(data= {"user_id": user.id})
    # RETURN TOKEN
    return Token(access_token=access_token, token_type= "bearer")