from app.model_runner import IrisModelRunner


def test_iris_model_runner_predicts_setosa() -> None:
    runner = IrisModelRunner()

    prediction = runner.predict([5.1, 3.5, 1.4, 0.2])

    assert prediction.class_id == 0
    assert prediction.label == "setosa"
