from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
#from sqlalchemy.exc import IntegrityError
from app.utils.hashing import hash_func
from app.utils.oauth2 import get_current_user
from app.database import get_db
from app.models import Vote, Post
from app.schemas import VoteSchema

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteSchema, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id: {vote.post_id} does not exist")
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote) #loads auto-gen fields
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exit")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}