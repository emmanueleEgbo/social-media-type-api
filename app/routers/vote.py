from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy import select
from app.session_settup import session
from sqlalchemy.exc import IntegrityError
from app.utils.hashing import hash_func
from app.utils.oauth2 import get_current_user
from app.session_settup import session
from app.models import Vote
from app.schemas import VoteSchema

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteSchema, current_user: int = Depends(get_current_user)):
    vote_query = session.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote) #loads auto-gen fields
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exit")
        vote_query.delete(synchronize_session=False)
        session.commit()

        return {"message": "successfully deleted vote"}