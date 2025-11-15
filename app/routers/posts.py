from typing import List, Optional
from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, Vote
from app.schemas import PostCreateSchema, PostSchema, PostOut
from app.utils.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[PostOut])
async def get_posts(current_user: int = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = ( 
        db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.id).filter(Post.content.contains(search)).limit(limit).offset(skip).all()
    )
    return [{"post": post, "votes": votes} for post, votes in results]

@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):

    post_query = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.id).where(Post.id == id)

    result = db.execute(post_query).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post, votes = result
    
    return {"post": post, "votes": votes}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(post: PostCreateSchema, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_post = Post(
            title=post.title,
            content=post.content,
            published=post.published,
            owner_id=current_user.id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post) #loads auto-gen fields
        return new_post
    except Exception as error:
       print("Unexpected Error:", str(error))
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Not authenticated."
       )
       

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post_to_delete = db.query(Post).filter(Post.id==id).first()

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exit!!!")  
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    
    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostSchema)
async def update_post(id: int, post: PostCreateSchema, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_post = db.query(Post).filter(Post.id == id).first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!!!") 
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    db.commit()
    db.refresh(existing_post)

    return existing_post