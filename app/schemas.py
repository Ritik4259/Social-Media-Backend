from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

       
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner : UserResponse

    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostOut(BaseModel):
    post : PostResponse
    votes : int
    
    model_config = ConfigDict(from_attributes=True)

# USER SCHEMAS


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]