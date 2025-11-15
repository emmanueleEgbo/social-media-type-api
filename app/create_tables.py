from app.models import Base, Post, User, Vote
from app.database import engine

print("CREATING TABLES >>>>>>>")
Base.metadata.create_all(bind=engine)