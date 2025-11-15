from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.config import settings



TEST_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.test_db_name}"
)

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the connection at startup
try:
    with engine.connect() as connection:
        result = connection.execute(text("select 'Hello'"))

        print(result.all())
    print("CONNECTION ESTABLISHED!!!")
except Exception as error:
    print("Database connection failed:", error)