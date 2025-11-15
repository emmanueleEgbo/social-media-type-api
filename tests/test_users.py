import pytest
import uuid
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    print("ROOT ENDPOINT TEST", res.json().get('message'))
    assert res.json().get('message') == 'Homepage! You are welcome!'
    assert res.status_code == 200

def test_create_user(client):
    """Create unique test user for auth tests always"""
    unique_email = f"luke_{uuid.uuid4().hex[:6]}@gmail.com"
    res = client.post("/users/", json={"email": unique_email, "password": "Password123"})

    assert res.status_code == 201
    assert "password" not in res.json()

    new_user = schemas.UserCreateReturnSchema(**res.json())
    assert new_user.email == unique_email

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.jwt_secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 201


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'Password123', 403),
    ('paul@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    ('', 'Password123', 422),
    ('paul@gmail.com', '', 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code