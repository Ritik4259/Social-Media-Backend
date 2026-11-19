from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..utils import security 
from sqlalchemy import select, delete

router = APIRouter(
    prefix="/vote",
    tags= ["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(database.get_db),
         current_user:int = Depends(security.get_current_user)):
    
    stmt = select(models.Post).where(models.Post.id==vote.post_id)
    
    post = db.execute(stmt).scalars().one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist"
        )
        
    stmt1 = select(models.Vote).where(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user
    )

    found_vote = db.execute(stmt1).scalar_one_or_none()
    
    if vote.dir==1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user} has alredy voted on post {vote.post_id}"
            )
            
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user)
        
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )
            
        delete_stmt = delete(models.Vote).where(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user
        )
            
        db.execute(delete_stmt)
        db.commit()
        
        return {"message":"Successfully deleted vote"}