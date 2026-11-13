from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import database, schemas, models, utils
from ..utils import security

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    stmt = select(models.User).where(models.User.email == user_credentials.username)

    user = db.execute(stmt).scalars().one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials"
        )

    if not security.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials"
        )
        
    access_token = security.create_access_token(data={'user_id':user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
