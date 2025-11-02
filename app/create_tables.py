from app.models import Base, Post, User, Vote
from app.db_connect import engine

print("CREATING TABLES >>>>>>>")
Base.metadata.create_all(bind=engine)