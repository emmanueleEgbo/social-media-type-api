from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from app.session_settup import session
from app.models import User
from app.schemas import TokenData, CurrentUser, UserInDB
from app.config import settings


JWT_SECRET_KEY_TEST=settings.jwt_secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expiry_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# HELPER FUNCTION
def get_user(user_id: int):
    result = result = select(User).where(User.id == user_id)
    user = session.scalars(result).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user_id}' is not found")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY_TEST, algorithm=ALGORITHM)
    return encoded_jwt

# VERIFY and Get Current User
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY_TEST, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[CurrentUser, Depends(get_current_user)],):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
    



