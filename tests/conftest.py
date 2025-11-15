from fastapi.testclient import TestClient
import pytest
import logging
from sqlalchemy import inspect
from app.main_w_sqlalchemy import app

from app.config import settings
from app.database import get_db
from app.utils.oauth2 import create_access_token
from app import models
from app.models import Base
from tests.database import engine, TestingSessionLocal


logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

inspector = inspect(engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("EXISTING TABLE", inspector.get_table_names())

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user2(client):
    # unique_email = f"john_{uuid.uuid4().hex[:6]}@gmail.com"
    unique_email = f"james@gmail.com"
    user_data = {"email": unique_email, "password": "Password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    """Create a unique test user for each test"""
    # unique_email = f"peter_{uuid.uuid4().hex[:6]}@gmail.com"
    unique_email = f"peter@gmail.com"
    user_data = {"email": unique_email, "password": "Password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers.update({
        #**client.headers.update,
        "Authorization": f"Bearer {token}"
    })

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
    {
        "title": "Building a REST API with FastAPI",
        "content": "An introduction to creating robust RESTful APIs using FastAPI and SQLAlchemy.",
        "owner_id": test_user['id']
    },
    {
        "title": "Testing FastAPI Applications with Pytest",
        "content": "A practical guide to setting up pytest fixtures and writing clean, isolated tests.",
        "owner_id": test_user['id']
    },
    {
        "title": "Deploying FastAPI to Production",
        "content": "Tips and best practices for deploying FastAPI apps with Docker and Gunicorn.",
        "owner_id": test_user['id']
    },
    {
        "title": "Advanced SQLAlchemy Relationships",
        "content": "Understanding one-to-many and many-to-many relationships using SQLAlchemy ORM.",
        "owner_id": test_user2['id']
    }]

    # def create_post_model(post):
    #     return models.Post(**post)
    
    # post_map = map(create_post_model, posts_data)
    # posts = list(post_map)

    posts = [models.Post(**data) for data in posts_data]
    session.add_all(posts)
    session.commit()

    for post in posts:
        session.refresh(post)
    return posts