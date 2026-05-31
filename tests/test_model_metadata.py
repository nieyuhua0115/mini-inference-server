from fastapi.testclient import TestClient

from app.main import app
from app.model_runner import IrisModelRunner


def test_iris_model_runner_metadata() -> None:
    runner = IrisModelRunner()

    metadata = runner.metadata()

    assert metadata.name == "iris-knn"
    assert metadata.version == "0.1.0"
    assert metadata.task == "classification"
    assert metadata.input_schema == {"features": "list[float] length 4"}
    assert metadata.output_schema == {"class_id": "int", "label": "str"}


def test_current_model_returns_metadata() -> None:
    with TestClient(app) as client:
        response = client.get("/models/current")

    assert response.status_code == 200
    assert response.json() == {
        "name": "iris-knn",
        "version": "0.1.0",
        "task": "classification",
        "input_schema": {
            "features": "list[float] length 4",
        },
        "output_schema": {
            "class_id": "int",
            "label": "str",
        },
    }
