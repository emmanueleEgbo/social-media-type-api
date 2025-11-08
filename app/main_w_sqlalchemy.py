from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, posts, auth, vote

app = FastAPI()

origins = ["*"] # SHOULD NARROWED-DOWN IN PROD

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
  return {"message": "Homepage! You are welcome!"}
