def test_register_login_and_profile(client):
    response = client.post("/auth/register", json={"full_name": "Staff User", "email": "staff@example.com", "password": "Password123", "role": "staff"})
    assert response.status_code == 201

    login = client.post("/auth/login", json={"email": "staff@example.com", "password": "Password123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    profile = client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
    assert profile.json()["email"] == "staff@example.com"
