from app.model_runner import DummyModelRunner


def test_dummy_model_runner_returns_input() -> None:
    runner = DummyModelRunner()

    assert runner.predict("hello") == "hello"
