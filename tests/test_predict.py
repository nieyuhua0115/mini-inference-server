from fastapi.testclient import TestClient

from app.main import app


def test_predict_returns_iris_prediction() -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})

    assert response.status_code == 200
    assert response.json() == {"class_id": 0, "label": "setosa"}


def test_predict_requires_features() -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={})

    assert response.status_code == 422


def test_predict_requires_four_features() -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={"features": [5.1, 3.5, 1.4]})

    assert response.status_code == 422
