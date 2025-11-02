from sqlalchemy.orm import Session
from app.db_connect import engine

session = Session(bind=engine)