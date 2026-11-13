from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..utils import security 


router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/",response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db),current_user: int = Depends(security.get_current_user)):
    stmt = select(models.User)

    users = db.execute(stmt).scalars().all()
    
    #print(current_user)

    return users

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.id==id)

    user = db.execute(stmt).scalars().one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user

@router.post("/create",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = security.hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user