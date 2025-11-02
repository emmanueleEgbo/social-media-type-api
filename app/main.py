import os
import time
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

# LOAD .env file
load_dotenv()

class PostModel(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None

# ASYNC Connection using CONNECTION POOLING
# DATABASE_URL = (
#   f"dbname={os.getenv("DB_NAME")}"
#   f"user={os.getenv("DB_USER")}"
#   f"password={os.getenv("DB_PASSWORD")}"
#   f"host={os.getenv("DB_HOST")}"
# )

# CONNECT to Database
def connect_to_db():
  max_retries = 10
  for attempt in range(max_retries):
    try:
      conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        autocommit=True
      )
      print("Connected to database successfully!")
      return conn
    except Exception as error:
      print(f"Attempt {attempt + 1}/{max_retries} failed: {error}")
      time.sleep(2 ** attempt)
  raise RuntimeError("Failed to connect to database after several attempts.")

# Using the connection we created
conn = connect_to_db()
print("conn Activated!")

# with conn.cursor(row_factory=dict_row) as cur:
#   cur.execute("SELECT * FROM posts ORDER BY id;")
#   rows = cur.fetchall()
#   for row in rows:
#     print(row)

POSTS = [
  {"title": "post#1 title", "content": "post#1 content", "id": 1},
  {"title": "post#2 title", "content": "post#2 content", "id": 2},
]

# HELPER Functions
def find_post(id): 
  for post in POSTS:
    if post['id'] == id:
      return post
  return None
    
def find_post_index(id):
  for i, post in enumerate(POSTS):
    if post['id'] == id:
      return i
  return None

@app.get("/")
async def root():
  return {"message": "Homepage! You are welcome!!!"}

@app.get("/posts")
async def get_posts():
  with conn.cursor(row_factory=dict_row) as cur:
    cur.execute("SELECT * FROM posts ORDER BY id;")
    posts = cur.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
async def get_post(id: int):
  with conn.cursor() as cur:
    cur.execute("""SELECT * FROM posts WHERE id = %s """, (id,)) # The comma ',' after id makes (id,) a 1 item turple. This solves this error: 'TypeError: query parameters should be a sequence or a mapping, got str'
    target_post = cur.fetchone()
    if not target_post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": target_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_tweets(post: PostModel):
  with conn.cursor() as cur:
    cur.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cur.fetchone()
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
  with conn.cursor() as cur:
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (id,))
    post_to_delete = cur.fetchone()

    if not post_to_delete:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exit!!!")  
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: PostModel):
  with conn.cursor() as cur:
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    
    updated_post = cur.fetchone()

    if updated_post is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!!!")
    
    return {"data": updated_post}
