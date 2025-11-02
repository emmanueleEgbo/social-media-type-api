from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
   title: str
   content: str
   published: bool = True


class PostCreateSchema(PostBase):
   pass 


class UserCreateSchema(BaseModel):
   email: EmailStr
   password: str


class UserCreateReturnSchema(BaseModel):
   id: int
   email: EmailStr
   created_at: datetime

   class Config:
      orm_mode = True


class PostSchema(PostBase):
   id: int
   created_at: datetime
   owner_id: int
   owner: UserCreateReturnSchema

   class Config:
      orm_mode = True

class PostOut(BaseModel):
   Post: PostSchema
   vote: int

   class Config:
      orm_mode = True

class UserLogin(BaseModel):
   email: EmailStr
   password: str

class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   id: Optional[int] | None = None

class CurrentUser(BaseModel):
   username: str
   email: EmailStr | None = None
   full_name: str | None = None
   disabled: bool | None = None
   id: int

class UserInDB(CurrentUser):
   hashed_password: str

class VoteSchema(BaseModel):
   post_id: int
   dir: Literal[0, 1]