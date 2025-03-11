from flask import json
from flask_security.utils import hash_password

#use appropriate test client and headers
def auth_headers(test_client):
    """Authenticate as admin and return headers with token."""
    response = test_client.post("/login", json={"email": "admin@test.com", "password": "password"})
    token = json.loads(response.data).get("auth_token")
    return {"Authentication-Token": token}


def test_deactivate_user(test_client, auth_headers):
    """
    Test deactivating a user.
    
    Test Input:
    {
        "user_id": 2
    }
    
    Expected Output:
    Status Code: 200
    JSON Response:
    {
        "message": "User testuser has been deactivated"
    }
    """
    response = test_client.post("/deactivate_user", json={"user_id": 2}, headers=auth_headers)
    assert response.status_code == 200
    assert "has been deactivated" in json.loads(response.data)["message"]


def test_activate_user(test_client, auth_headers):
    """
    Test activating a user.
    
    Test Input:
    {
        "user_id": 2
    }
    
    Expected Output:
    Status Code: 200
    JSON Response:
    {
        "message": "User testuser has been activated"
    }
    """
    response = test_client.post("/activate_user", json={"user_id": 2}, headers=auth_headers)
    assert response.status_code == 200
    assert "has been activated" in json.loads(response.data)["message"]


def test_list_users_excludes_admin(test_client, auth_headers):
    """
    Test that listing users does not include admins.
    
    Test Input: None
    
    Expected Output:
    Status Code: 200
    JSON Response:
    [
        {
            "id": 2,
            "username": "testuser",
            "email": "user@test.com",
            "active": true
        }
    ]
    """
    response = test_client.get("/list_users", headers=auth_headers)
    assert response.status_code == 200
    users = json.loads(response.data)
    assert all(user["username"] != "admin" for user in users)