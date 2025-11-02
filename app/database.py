import os
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, relationship
from app.config import settings

DATABASE_URL = settings.db_url
engine = create_engine(DATABASE_URL, future=True)

class Base(DeclarativeBase):
  pass