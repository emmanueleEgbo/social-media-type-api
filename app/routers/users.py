from fastapi import HTTPException, status, Response, APIRouter
from sqlalchemy import select
from app.session_settup import session
from sqlalchemy.exc import IntegrityError
from app.utils.hashing import hash_func
from app.session_settup import session
from app.models import User
from app.schemas import UserCreateSchema, UserCreateReturnSchema

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateReturnSchema)
def create_user(user: UserCreateSchema):
    try:
        password_hash = hash_func(user.password)
        new_user = User(
          email=user.email,
          password=password_hash
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user) #loads auto-gen fields
        print("Post created!!!", new_user.id)
        return new_user
    except IntegrityError:
       session.rollback()
       raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"User with email '{user.email}' already exists.",
       )
    except Exception as error:
       print("Failed to create user", error)
       return error
  

@router.get("/{id}", response_model=UserCreateReturnSchema)
def get_user(id: int):
    result = select(User).where(User.id == id)
    target_user = session.scalars(result).first()
    if target_user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return  target_user