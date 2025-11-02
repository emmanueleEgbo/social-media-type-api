from typing import List, Optional
from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import select, func
from app.session_settup import session
from app.models import Post, Vote
from app.schemas import PostCreateSchema, PostSchema, PostOut
from app.utils.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[PostOut])
async def get_posts(current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # all_posts = session.query(Post).filter(Post.title.contains(search)).order_by(Post.id).limit(limit).offset(offset=skip).all()

    results = session.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.id).filter(Post.content.contains(search)).limit(limit).offset(skip).all()
    
    return [{"Post": post, "vote": vote} for post, vote in results]

@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, current_user: int = Depends(get_current_user)):
    # result = select(Post).where(Post.id == id)

    post_query = session.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.id).where(Post.id == id)

    result = session.execute(post_query).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post, votes = result
    
    return {"Post": post, "vote": votes}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(post: PostCreateSchema, current_user: int = Depends(get_current_user)):
    try:
        print("USER ID", current_user.id)
        new_post = Post(
          title=post.title,
          content=post.content,
          published=post.published,
          owner_id=current_user.id
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post) #loads auto-gen fields
        return new_post
    except Exception as error:
       print("Unexpected Error:", str(error))
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Not authenticated."
       )
       

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: int = Depends(get_current_user)):
    post_to_delete = session.query(Post).filter_by(id=id).first()

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exit!!!")  
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    
    session.delete(post_to_delete)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostSchema)
async def update_post(id: int, post: PostCreateSchema, current_user: int = Depends(get_current_user)):
    updated_post = session.query(Post).filter_by(id=id).first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!!!") 
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    
    updated_post.title = post.title
    updated_post.content = post.content
    updated_post.published = post.published
    session.commit()
    session.refresh(updated_post)

    return updated_post