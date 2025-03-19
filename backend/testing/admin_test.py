import pytest
import json
from app import app

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def auth_headers(test_client):
    response = test_client.post('/signin', json={
        "email": "admin@a.com",
        "password": "admin"
    })
    data = response.get_json()
    token = data.get("token")
    assert token is not None, "No auth_token received from login."
    return {"Authorization": token}

@pytest.fixture
def non_admin_auth_headers(test_client):
    response = test_client.post('/signin', json={
        "email": "user@a.com",
        "password": "user"
    })
    data = response.get_json()
    token = data.get("token")
    assert token is not None, "No auth_token received from login."
    return {"Authorization": token}

def test_deactivate_user_success(test_client, auth_headers):
    response = test_client.post(
        "/admin/user/deactivate",
        json={"user_id": 2},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "has been deactivated" in response.json["message"]

def test_deactivate_user_missing_id(test_client, auth_headers):
    response = test_client.post("/admin/user/deactivate", json={}, headers=auth_headers)
    assert response.status_code == 400
    assert response.get_json()["error"] == "User ID is required"

def test_deactivate_user_not_found(test_client, auth_headers):
    response = test_client.post("/admin/user/deactivate", json={"user_id": 999}, headers=auth_headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

def test_activate_user_success(test_client, auth_headers):
    response = test_client.post(
        "/admin/user/activate",
        json={"user_id": 2},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "has been activated" in response.get_json()["message"]

def test_activate_user_missing_id(test_client, auth_headers):
    response = test_client.post("/admin/user/activate", json={}, headers=auth_headers)
    assert response.status_code == 400
    assert response.get_json()["error"] == "User ID is required"

def test_activate_user_not_found(test_client, auth_headers):
    response = test_client.post("/admin/user/activate", json={"user_id": 999}, headers=auth_headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

def test_admin_list_users_excludes_admin(test_client, auth_headers):
    response = test_client.get("/admin/user/list", headers=auth_headers)
    assert response.status_code == 200
    users = response.get_json()
    assert all(user["username"] != "admin" for user in users)

def test_unauthorized_deactivate_user(test_client):
    response = test_client.post("/admin/user/deactivate", json={"user_id": 2})
    assert response.status_code == 401

def test_non_admin_cannot_deactivate_user(test_client, non_admin_auth_headers):
    response = test_client.post("/admin/user/deactivate", json={"user_id": 2}, headers=non_admin_auth_headers)
    assert response.status_code == 403

def test_unauthorized_activate_user(test_client):
    response = test_client.post("/admin/user/activate", json={"user_id": 2})
    assert response.status_code == 401

def test_non_admin_cannot_activate_user(test_client, non_admin_auth_headers):
    response = test_client.post("/admin/user/activate", json={"user_id": 2}, headers=non_admin_auth_headers)
    assert response.status_code == 403


def test_non_admin_cannot_list_users(test_client, non_admin_auth_headers):
    response = test_client.get("/admin/user/list", headers=non_admin_auth_headers)
    assert response.status_code == 403
