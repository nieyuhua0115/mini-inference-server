from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_predict_returns_input_as_output() -> None:
    response = client.post("/predict", json={"input": "hello"})

    assert response.status_code == 200
    assert response.json() == {"output": "hello"}


def test_predict_requires_input() -> None:
    response = client.post("/predict", json={})

    assert response.status_code == 422
