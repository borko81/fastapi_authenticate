from fastapi.testclient import TestClient


from userapp.main import app

client = TestClient(app)


def test_get_all_users():
    response = client.get("/app/users/users")
    assert response.status_code == 200
