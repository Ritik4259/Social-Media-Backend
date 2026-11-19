from fastapi import status, HTTPException, Depends, APIRouter, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import security

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
):

    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    if search:
        stmt = stmt.where(models.Post.title.contains(search))

    stmt = stmt.limit(limit).offset(offset)

    posts = [
        {"post": post, "votes": votes}
        for post, votes in db.execute(stmt).all()
    ]

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .where(models.Post.id == id)
    )

    row = db.execute(stmt).one_or_none()
    post = row[0] if row is not None else None
    votes = row[1] if row is not None else None

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return {"post": post, "votes": votes}


@router.post(
    "/create", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    new_post = models.Post(owner_id=current_user, **post.model_dump())

    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    stmt = select(models.Post).where(models.Post.id == id)

    deleted_post = db.execute(stmt).scalar_one_or_none()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found",
        )

    if deleted_post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    db.delete(deleted_post)
    db.commit()

    return {"message": f"Post with {id} deleted"}


@router.patch("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(security.get_current_user),
):

    stmt = select(models.Post).where(models.Post.id == id)

    upd_post = db.execute(stmt).scalar_one_or_none()

    if upd_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found"
        )

    update_data = post.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    if upd_post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    for key, value in update_data.items():
        setattr(upd_post, key, value)

    db.commit()
    db.refresh(upd_post)

    return upd_post
