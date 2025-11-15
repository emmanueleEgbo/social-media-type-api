from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils.hashing import hash_func
from app.database import get_db
from app.models import User
from app.schemas import UserCreateSchema, UserCreateReturnSchema

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateReturnSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        password_hash = hash_func(user.password)
        new_user = User(
          email=user.email,
          password=password_hash
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user) #loads auto-gen fields
        return new_user
    except IntegrityError:
       db.rollback()
       raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"User with email '{user.email}' already exists.",
       )
    except Exception as error:
       print("Failed to create user", error)
       return error
  

@router.get("/{id}", response_model=UserCreateReturnSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    result = select(User).where(User.id == id)
    target_user = db.query(result).first()
    if target_user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return  target_user