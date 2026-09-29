from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)


# API
def test_api():
    response = client.get("/docs")
    assert response.status_code == 200


# Get
def test_get_user_without_token():
    response = client.get("/users")
    assert response.status_code == 401


def test_get_users_authenticated(test_manager):
    token =  create_access_token(test_manager.id)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    data = response.json()
    assert any(user["id"] == test_manager.id for user in data)


def test_get_user_by_id(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Post
def test_create_user():
    response = client.post(
    "/users",
    params={"name":"Test2",
          "email":"test2@example.com",
          "password":"Test123",
          }
    )
    assert response.status_code == 200


def test_create_user_missing_password():
    response = client.post(
    "/users",
    params={
        "name":"Test",
        "email":"Test@example.com"
    }
    )
    assert response.status_code == 422


# Patch
def test_update_user(test_user):
    response = client.patch(
        f"/users/{test_user.id}",
         json={
            "name": "New name",
             "email": "newemail@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"id":test_user.id ,"name": "New name", "email": "newemail@example.com"}


def test_update_user_not_found():
    response = client.patch(
        "/users/999",
        json={
            "name" : "New Name",
            "email" : "newemail@example.com"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Delete
def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user():
    response = client.post(
        "/users",
        params={
            "name" : "Test",
            "email" : "Test@example.com",
            "password" : "Test1234",
        })
    user_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json() == {
        "id" : user_id ,
        "name" : "Test" ,
        "email" : "Test@example.com"
    }
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Login
def test_login_success(login_user):
    response = client.post(
        "/login",
        json={
            "email": login_user.email,
            "password": "Test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()
    assert isinstance(token, str)
    assert len(token) > 0


def test_login_wrong_password(login_user):
    response = client.post(
        "/login",
        json={
            "email": login_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_wrong_email(login_user):
    response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "Test1234"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_missing_fields():
    response = client.post(
        "/login",
        json={}
    )
    assert response.status_code == 422


# Patch Role
def test_update_role(test_manager):
    token = create_access_token(test_manager.id)
    response = client.patch(
        f"/users/{test_manager.id}/role",
        headers={"Authorization": f"Bearer {token}"},

        json={
            "role": "customer"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_manager.id
    assert data["name"] == test_manager.name
    assert data["email"] == test_manager.email


def test_update_incorrect_role(test_user):
    token = create_access_token(test_user.id)
    response = client.patch(
        f"/users/{test_user.id}/role",
        headers={"Authorization": f"Bearer {token}"},

        json={
            "role": "customer"
        }
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Incorrect role"}


def test_update_role_user_not_found():
    token = create_access_token(999)
    response = client.patch(
        "/users/999/role",
        headers={"Authorization": f"Bearer {token}"},

        json={
            "role": "customer"
        }
    )
    assert response.status_code == 401


def test_update_role_user_without_token():
    response = client.patch(
        "/users/999/role",

        json={
            "role": "customer"
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

