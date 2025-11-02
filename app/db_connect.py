from sqlalchemy import create_engine, text
from app.config import settings


SQLALCHEMY_DB_URL=settings.db_url
engine = create_engine(SQLALCHEMY_DB_URL, echo=True)

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("select 'Hello'"))

        print(result.all())
    print("CONNECTION ESTABLISHED!!!")
except Exception as error:
    print("Database connection failed:", error)